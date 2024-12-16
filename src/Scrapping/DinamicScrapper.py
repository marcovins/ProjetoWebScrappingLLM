from bs4 import BeautifulSoup
from src.Schemas.ResponseSchema import ResponseSchema
from src.Utils.http_utils import make_request_to_model, exist_cookies, contains_cookie_terms
from scrapegraphai.graphs import SmartScraperGraph
from src.Utils.imports import PROMPT, GRAPH_CONFIG, COOKIES
from src.Utils.driver_utils import setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging, json, re, time, os

from src.Utils.json_utils import limpar_json

def StaticScrapper(url: str) -> dict | None:
    """
    Realiza scraping estático de uma URL utilizando a biblioteca SmartScraperGraph.

    Args:
        url (str): URL a ser processada.

    Returns:
        dict: Dados extraídos da URL.
    """
    try:
        smart_scraper_graph = SmartScraperGraph(
            prompt=PROMPT,
            source=url,
            config=GRAPH_CONFIG,
            schema=ResponseSchema
        )
        return smart_scraper_graph.run()
    except Exception as e:
        logging.error("Erro no scraper estático: %s", str(e))
        return None

def getSource(url: str) -> str:
    """
    Obtém o HTML da página utilizando Selenium.

    Args:
        url (str): URL da página a ser acessada.

    Returns:
        str: HTML da página carregada.
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
    Filtra sequências específicas de um texto, removendo URLs e strings com 
    pelo menos 40 caracteres alfanuméricos consecutivos. Além disso, reduz 
    espaços consecutivos para um único espaço.

    Args:
        texto (str): Texto de entrada a ser processado.

    Returns:
        str: Texto filtrado, sem URLs, sem sequências alfanuméricas longas e 
        com espaçamento normalizado.
    """
    padrao = r"(https?:\/\/\S+)|(\b[a-zA-Z0-9_\-]{40,}\b)"
    texto_filtrado = re.sub(padrao, "", texto)
    texto_filtrado = re.sub(r"\s{2,}", " ", texto_filtrado)
    return texto_filtrado.strip()

def parseHTML(html: str) -> dict:
    """
    Processa o HTML extraído e organiza os dados.

    Args:
        html (str): HTML da página a ser processado.

    Returns:
        dict: Dados extraídos, incluindo título, meta descrição e parágrafos.
    """
    data = {}

    # Continue com o resto da análise do HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extração de dados padrão
    title = filtrar_sequencias(soup.find('title').text) if soup.find('title') else None
    if title:
        data['title'] = title

    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        data['meta_description'] = filtrar_sequencias(meta_description.get('content', ''))

    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords:
        data['meta_keywords'] = filtrar_sequencias(meta_keywords.get('content', ''))

    favicon = soup.find('link', rel='icon')
    if favicon:
        data['favicon'] = filtrar_sequencias(favicon.get('href', ''))

    # tags p, h1, h2
    p_tags = [filtrar_sequencias(tag.text) for tag in soup.find_all('p') if not contains_cookie_terms(tag.text)]
    if p_tags:
        data['p_tags'] = p_tags

    h1_tags = [filtrar_sequencias(tag.text) for tag in soup.find_all('h1') if not contains_cookie_terms(tag.text)]
    if h1_tags:
        data['h1_tags'] = h1_tags

    h2_tags = [filtrar_sequencias(tag.text) for tag in soup.find_all('h2') if not contains_cookie_terms(tag.text)]
    if h2_tags:
        data['h2_tags'] = h2_tags

    images = [{'src': filtrar_sequencias(img['src']), 'alt': filtrar_sequencias(img.get('alt', 'Sem descrição'))}
              for img in soup.find_all('img', src=True)]
    if images:
        data['images'] = images

    return data

def to_markdown(data: dict) -> str:
    """
    Converte os dados processados em formato Markdown.

    Args:
        data (dict): Dados extraídos da página.

    Returns:
        str: Conteúdo em formato Markdown.
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

    return markdown

def HandlerDinamic(url: str, prompt: str = PROMPT) -> dict | None:
    """
    Realiza scraping dinâmico utilizando Selenium e converte o resultado.

    Args:
        url (str): URL da página a ser processada.
        prompt (str): Prompt para o modelo de processamento de linguagem.

    Returns:
        dict: Resultado do scraping processado.
    """
    html = getSource(url)

    if html:
        data = parseHTML(html)
        markdown = to_markdown(data)
        return make_request_to_model(markdown)
    return None
