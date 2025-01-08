import aiofiles
from bs4 import BeautifulSoup
from src.Utils.http_utils import make_request_to_model, exist_cookies, contains_cookie_terms
from src.Utils.imports import PROMPT, COOKIES, SCRAPS
from src.Utils.driver_utils import setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging, json, re, time, os

from src.Utils.json_utils import limpar_json


def getSource(url: str) -> str:
    """
    Obtém o HTML de uma página web utilizando o Selenium, garantindo que cookies sejam 
    aceitos e carregados corretamente, simulando scroll para garantir o carregamento completo da página.

    A função executa as seguintes etapas:
    1. Configura o driver do Selenium.
    2. Verifica se já existem cookies salvos para a URL fornecida.
    3. Caso os cookies não existam, acessa a página para coletá-los e aceita o pop-up de cookies, se presente.
    4. Adiciona os cookies salvos ao driver e recarrega a página com os cookies aplicados.
    5. Aguarda o carregamento completo da página e simula o scroll para garantir que todo o conteúdo seja carregado.
    6. Retorna o HTML da página após o carregamento completo.

    Parâmetros:
    url (str): A URL da página web a ser acessada e carregada.

    Retorna:
    str: O código HTML da página carregada com sucesso, ou None caso ocorra algum erro no processo.

    Exceções:
    - Caso haja erro na execução de qualquer uma das etapas, um erro será registrado e a função retornará None.

    Exemplo de uso:
    ```python
    html = getSource("https://example.com")
    if html:
        print(html)
    else:
        print("Erro ao carregar a página.")
    ```

    Observações:
    - A função depende da configuração de um driver Selenium, que deve ser configurado previamente com a função `setup_driver()`.
    - O processo de aceitação de cookies pode ser ignorado se o botão não for encontrado, mas a função continuará a tentar carregar a página.
    - O arquivo de cookies é salvo localmente para evitar a necessidade de nova coleta para páginas que já foram acessadas.
    - A função simula scroll até o final da página e de volta ao topo para garantir que o conteúdo dinâmico seja totalmente carregado antes de extrair o HTML.

    Logs:
    - Logs informativos sobre o status da coleta de cookies, aceitação do pop-up de cookies, e erros durante o processo de carregamento da página.
    """
    
    driver = None
    try:
        # Configura o driver
        driver = setup_driver()

        # Abrir uma página em branco para poder adicionar cookies
        driver.get("about:blank")

        # Verifique se os cookies já existem para a URL
        page_cookies = exist_cookies(url)
        if not page_cookies:
            logging.info("Site sem cookies...")

            # Se não existir, acessar a página para coletar os cookies
            driver.get(url)
            
            # Aguarde e clique no botão de aceitação do pop-up de cookies, se ele aparecer
            try:
                wait = WebDriverWait(driver, 10)
                accept_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Aceito"]'))
                )
                accept_button.click()
                logging.info("Botão de aceitação de cookies encontrado e clicado.")
                WebDriverWait(driver, 5).until(
                    EC.staleness_of(accept_button)
                )

            except Exception as cookie_error:
                logging.warning("Não foi possível encontrar o botão de aceitação de cookies. Continuando sem clicar...")

            finally:
                cookies = driver.get_cookies()
                cookie_file = f"{COOKIES}/{url.replace('://', '_').replace('/', '_')}_cookies.json"
                with open(cookie_file, "w") as file:
                    json.dump(cookies, file)

        else:
            logging.info("Cookies encontrados...")
            # Se os cookies já existirem, carregue-os
            cookie_file = page_cookies
            if os.path.exists(cookie_file):
                with open(cookie_file, "r") as file:
                    cookies = json.load(file)
                    driver.get(url)

                    # Adicionar os cookies carregados
                    for cookie in cookies:
                        try:
                            driver.add_cookie(cookie)
                            logging.info(f"Cookie adicionado: {cookie}")
                        except Exception as e:
                            logging.warning(f"Erro ao adicionar cookie: {e}")

        # Agora, carregue a página com os cookies já aplicados
        driver.refresh()

        # Espera até que a página carregue completamente
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Simular scroll até o final
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 3).until(
            lambda d: d.execute_script("return document.body.scrollHeight") > 0
        )

        # Simular scroll de volta ao topo
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Retorna o HTML da página
        return driver.page_source

    except Exception as e:
        logging.error(f"Erro ao carregar a página {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def filtrar_sequencias(texto: str) -> str:
    """
    Filtra sequências específicas de um texto, removendo URLs e strings alfanuméricas 
    com pelo menos 40 caracteres consecutivos. Além disso, normaliza espaços consecutivos 
    para um único espaço.

    Esta função realiza duas principais modificações no texto:
    1. Remove URLs que começam com "http" ou "https".
    2. Remove sequências alfanuméricas longas (com pelo menos 40 caracteres consecutivos).
    3. Substitui múltiplos espaços consecutivos por um único espaço.

    Parâmetros:
    texto (str): O texto de entrada a ser processado. Pode conter URLs, sequências alfanuméricas longas 
                 ou espaços excessivos que precisam ser removidos.

    Retorna:
    str: O texto filtrado, sem URLs, sem sequências alfanuméricas longas e com espaçamento normalizado 
         (apenas um espaço entre palavras e sem espaços no início ou no final).

    Exemplos:
    ```python
    texto_original = "Visite https://exemplo.com para mais informações. Lorem ipsum dolor sit amet."
    texto_filtrado = filtrar_sequencias(texto_original)
    # Saída: "Visite para mais informações. Lorem ipsum dolor sit amet."
    ```

    Observações:
    - A função usa expressões regulares (regex) para identificar URLs e sequências alfanuméricas longas.
    - Após a remoção das sequências indesejadas, a função normaliza os espaços no texto, eliminando espaços extras.
    - O texto retornado está sem espaços no início ou no final, após o uso de `.strip()`.

    Logs:
    A função não gera logs diretamente, mas pode ser usada para pré-processamento de dados em outras funções de logging.
    """
    padrao = r"(https?:\/\/\S+)|(\b[a-zA-Z0-9_\-]{40,}\b)"
    texto_filtrado = re.sub(padrao, "", texto)
    texto_filtrado = re.sub(r"\s{2,}", " ", texto_filtrado)
    return texto_filtrado.strip()

def parseHTML(html: str) -> dict:
    """
    Processa o HTML extraído de uma página e organiza os dados relevantes em um dicionário.

    Esta função utiliza a biblioteca BeautifulSoup para analisar o HTML de uma página e extrair informações importantes,
    como título da página, meta descrição, palavras-chave, favicon, tags de parágrafos, títulos (h1, h2) e imagens. 
    Os dados extraídos são retornados em um dicionário estruturado.

    Parâmetros:
    html (str): O conteúdo HTML da página a ser processado. Deve ser uma string contendo o código HTML da página.

    Retorna:
    dict: Um dicionário contendo os dados extraídos do HTML. Os dados podem incluir:
          - 'title': O título da página.
          - 'meta_description': A meta descrição da página.
          - 'meta_keywords': As palavras-chave associadas à página.
          - 'favicon': A URL do favicon da página.
          - 'p_tags': Lista de parágrafos extraídos da página.
          - 'h1_tags': Lista de tags H1 extraídas da página.
          - 'h2_tags': Lista de tags H2 extraídas da página.
          - 'images': Lista de dicionários contendo as URLs das imagens e seus atributos 'alt'.

    Exemplos:
    ```python
    html_content = "<html><head><title>Example</title></head><body><p>Texto de exemplo</p></body></html>"
    data = parseHTML(html_content)
    ```

    Observações:
    - A função usa `filtrar_sequencias` para limpar o conteúdo de texto extraído, removendo caracteres indesejados.
    - As tags de parágrafos, h1 e h2 são filtradas para garantir que não contenham termos relacionados a cookies.
    - As imagens extraídas incluem suas URLs (atributo 'src') e descrições alternativas (atributo 'alt').
    - Caso não existam elementos correspondentes (ex. 'title', 'meta_description', etc.), esses campos são omitidos do dicionário retornado.

    Logs:
    A função não gera logs diretamente, mas os resultados podem ser usados posteriormente em outras funções de logging.
    """
    data = {}

    # Continue com o resto da análise do HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Função para verificar se o conteúdo não é vazio ou só contém espaços
    def is_not_empty(content):
        return bool(content.strip())

    # Extração de dados padrão
    title = filtrar_sequencias(soup.find('title').text) if soup.find('title') else None
    if title and is_not_empty(title):
        data['title'] = title

    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        description = filtrar_sequencias(meta_description.get('content', ''))
        if is_not_empty(description):
            data['meta_description'] = description

    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords:
        keywords = filtrar_sequencias(meta_keywords.get('content', ''))
        if is_not_empty(keywords):
            data['meta_keywords'] = keywords

    favicon = soup.find('link', rel='icon')
    if favicon:
        favicon_url = filtrar_sequencias(favicon.get('href', ''))
        if is_not_empty(favicon_url):
            data['favicon'] = favicon_url

    # tags p, h1, h2
    p_tags = [filtrar_sequencias(tag.text) for tag in soup.find_all('p') if not contains_cookie_terms(tag.text)]
    if p_tags and any(is_not_empty(tag) for tag in p_tags):
        data['p_tags'] = [tag for tag in p_tags if is_not_empty(tag)]

    h1_tags = [filtrar_sequencias(tag.text) for tag in soup.find_all('h1') if not contains_cookie_terms(tag.text)]
    if h1_tags and any(is_not_empty(tag) for tag in h1_tags):
        data['h1_tags'] = [tag for tag in h1_tags if is_not_empty(tag)]

    h2_tags = [filtrar_sequencias(tag.text) for tag in soup.find_all('h2') if not contains_cookie_terms(tag.text)]
    if h2_tags and any(is_not_empty(tag) for tag in h2_tags):
        data['h2_tags'] = [tag for tag in h2_tags if is_not_empty(tag)]

    images = [{'src': filtrar_sequencias(img['src']), 'alt': filtrar_sequencias(img.get('alt', 'Sem descrição'))}
            for img in soup.find_all('img', src=True)]
    if images:
        data['images'] = [img for img in images if is_not_empty(img['src'])]

    return data

async def to_markdown(data: dict, url:str) -> str:
    """
    Converte os dados extraídos de uma página em um formato Markdown.

    Esta função pega os dados extraídos de uma página web (como título, meta descrição, palavras-chave,
    tags de cabeçalho, parágrafos e imagens) e os organiza em um conteúdo estruturado em formato Markdown. 
    O conteúdo gerado é salvo em um arquivo `.md` no diretório de markdowns e também retornado como string.

    Parâmetros:
    data (dict): Um dicionário contendo os dados extraídos da página, que pode incluir:
                 - 'title': Título da página.
                 - 'meta_description': Descrição meta da página.
                 - 'meta_keywords': Palavras-chave meta da página.
                 - 'h1_tags': Lista de títulos de nível H1.
                 - 'h2_tags': Lista de títulos de nível H2.
                 - 'p_tags': Lista de parágrafos da página.
                 - 'images': Lista de imagens com atributos 'alt' e 'src'.
                 - 'favicon': URL do favicon da página.
    url (str): A URL da página, usada para criar o nome do arquivo Markdown.

    Retorna:
    str: O conteúdo gerado em formato Markdown.

    Exceções:
    Nenhuma exceção explícita é levantada, mas pode haver falha ao salvar o arquivo se houver problemas 
    com o diretório de destino ou permissões de escrita.

    Exemplos:
    ```python
    markdown_content = await to_markdown(data, 'https://example.com')
    ```

    Logs:
    A função imprime "Scraping concluído com sucesso!" ao concluir a conversão para Markdown e salvar o arquivo.
    """
    markdown = ""

    # Adicionando o título
    if 'title' in data:
        markdown += f"# {data['title']}\n\n"

    # Adicionando a meta descrição
    if 'meta_description' in data:
        markdown += f"**Descrição**: {data['meta_description']}\n\n"

    # Adicionando as palavras-chave
    if 'meta_keywords' in data:
        markdown += f"**Palavras-chave**: {data['meta_keywords']}\n\n"

    # Adicionando as tags de cabeçalho h1
    if 'h1_tags' in data:
        for h1 in data['h1_tags']:
            markdown += f"## {h1}\n\n"

    # Adicionando as tags de cabeçalho h2
    if 'h2_tags' in data:
        for h2 in data['h2_tags']:
            markdown += f"### {h2}\n\n"

    # Adicionando os parágrafos
    if 'p_tags' in data:
        for p in data['p_tags']:
            markdown += f"{p}\n\n"

    # Adicionando as imagens
    if 'images' in data:
        for image in data['images']:
            markdown += f"![{image['alt']}]({image['src']})\n\n"

    # Adicionando o favicon (se houver)
    if 'favicon' in data:
        markdown += f"**Favicon**: ![{data['favicon']}]({data['favicon']})\n\n"

    # Salvar em um arquivo
    async with aiofiles.open(f"{SCRAPS}/markdowns/{url.replace('/', '').replace('https:', '')}.md", "w", encoding="utf-8") as arquivo:
        await arquivo.write(markdown)
        print("Scraping concluído com sucesso!")

    return markdown

async def HandlerDinamic(url: str, prompt: str = PROMPT, source:str = None) -> dict:
    """
    Processa o conteúdo HTML de uma página ou fonte fornecida e envia para um modelo de IA para análise.

    A função busca o conteúdo HTML de uma página da web ou usa uma fonte HTML fornecida e, em seguida,
    envia os dados para um modelo de IA para processamento. Caso o processamento seja bem-sucedido, 
    os resultados são retornados em formato de dicionário. Se ocorrer algum erro durante a comunicação 
    com o modelo ou ao processar o HTML, a função registra o erro nos logs e retorna `None`.

    Parâmetros:
    url (str): A URL da página da web a ser processada. Necessário caso `source` não seja fornecido.
    prompt (str, opcional): O prompt que será usado ao interagir com o modelo de IA. O valor padrão é definido por `PROMPT`.
    source (str, opcional): Uma string contendo o código HTML a ser processado. Se não fornecido, o conteúdo será recuperado da URL.

    Retorna:
    dict ou None: O resultado do modelo em formato de dicionário se o processamento for bem-sucedido; 
                   caso contrário, `None`.

    Exceções:
    Nenhuma exceção explícita é levantada, mas erros de comunicação com o modelo ou processamento do HTML
    são registrados nos logs.

    Exemplo:
    ```python
    result = await HandlerDinamic('https://example.com')
    result = await HandlerDinamic('https://example.com', source='<html><body><p>Conteúdo</p></body></html>')
    ```

    Logs:
    A função registra erros no log caso ocorra falha na comunicação com o modelo ou no processamento do HTML.
    """
    if source:
        html = source
    else:
        html = getSource(url)

    if html:
        data = parseHTML(html)
        
        result = await make_request_to_model(data)

        if result:
            return result
        else:
            logging.error("Erro na comunicação com o modelo.")
            return None
    return None