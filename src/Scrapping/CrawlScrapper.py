from crawl4ai import AsyncWebCrawler
from src.Scrapping.DinamicScrapper import getSource, to_markdown, parseHTML, HandlerDinamic
import logging
import aiofiles
from src.Utils.imports import SCRAPS
import re

async def CrawlScrapper(source: str, verbose: bool = False, timeout: int = 30 , markdown:bool = False) -> dict:
    """
    Realiza o scraping dinâmico de uma página da web usando a biblioteca AsyncWebCrawler do crawl4ai.

    A função acessa a URL fornecida e realiza scraping dinâmico, coletando dados da página de forma assíncrona. 
    É possível configurar se o scraping será realizado com logs detalhados, se será feito um processamento de markdown ou 
    se um tempo limite será imposto para a operação. A função suporta a obtenção do conteúdo da página em formato Markdown ou como um dicionário com detalhes do scraping.

    Parâmetros:
    source (str): URL da página a ser acessada. A URL deve começar com 'http://' ou 'https://'.
    verbose (bool, opcional): Define se os logs detalhados devem ser exibidos durante a execução. O valor padrão é False.
    timeout (int, opcional): Tempo limite para a operação em segundos. O valor padrão é 30.
    markdown (bool, opcional): Se True, retorna o conteúdo da página em formato Markdown. Caso contrário, retorna um dicionário com dados detalhados do scraping. O valor padrão é False.

    Retorna:
    dict | None: 
        - Se `markdown` for True: Retorna o conteúdo da página em formato Markdown, caso tenha sido extraído com sucesso.
        - Se `markdown` for False: Retorna um dicionário com informações detalhadas do scraping, incluindo HTML e outros metadados.
        - None: Caso ocorra um erro durante o processo de scraping ou processamento.

    Levanta Exceções:
    ValueError: Se o argumento `source` não for uma string válida ou não começar com 'http://' ou 'https://'.
    Exception: Caso ocorra um erro inesperado durante a operação de scraping.

    Exemplo de uso:
    ```python
    result = asyncio.run(CrawlScrapper(source="https://www.example.com", markdown=True))
    print(result)
    ```

    Observações:
    - A função utiliza o `AsyncWebCrawler` da biblioteca `crawl4ai` para realizar scraping assíncrono da página.
    - O parâmetro `verbose` permite visualizar logs detalhados durante o scraping, útil para depuração.
    - O parâmetro `markdown` permite retornar o conteúdo da página em formato Markdown. Se False, o conteúdo será retornado em formato de dicionário.
    - Caso o conteúdo extraído em Markdown esteja vazio ou inválido, a função pode tentar realizar um scraping dinâmico adicional.
    - A função também suporta o processamento de iframes, remoção de elementos de sobreposição e outros ajustes para otimizar a coleta de dados.

    Logs:
    - A função gera logs em caso de erros durante o scraping ou extração do conteúdo.
    """
    try:
        # Criar a instância do crawler corretamente com o parâmetro verbose
        async with AsyncWebCrawler(verbose=verbose, headless=True, sleep_on_close=True) as crawler:

            result = await crawler.arun(
                url=source,
                # Configurações básicas
                exclude_external_links=True,
                fit_markdown=True,
                headless=True,

                # Parâmetros opcionais para testar
                word_count_threshold=5,
                excluded_tags=['form', 'header'],
                process_iframes=True,
                remove_overlay_elements=True,
                magic=True,
                simulate_user=True,
                override_navigator=True,
                page_timeout=60000,

                # Cache e timeout
                bypass_cache=False,
                timeout=30,
                delay_before_return_html=3.0,  # Aguardar mais tempo antes de capturar o HTML
                sleep_on_close= True,

            )
            
            if result:
                if markdown:
                    # Conteúdo da variável
                    try:
                        conteudo = result.markdown

                        # Substituir quebras de linha por <br> no conteúdo (se for para HTML)
                        conteudo = conteudo.replace("\n", "<br>")

                        # Verificar se o conteúdo é vazio ou contém apenas espaços/br
                        if not re.fullmatch(r"(\s|<br>)*", conteudo):  # Inversão da lógica para salvar apenas conteúdo válido
                            try:
                                # Salvar em um arquivo
                                async with aiofiles.open(
                                    f"{SCRAPS}/markdowns/{source.replace('/', '').replace('https:', '')}.md",
                                    "w",
                                    encoding="utf-8",
                                ) as arquivo:
                                    await arquivo.write(conteudo)
                                    print("Scraping concluído com sucesso!")
                            except:
                                pass
                            finally:
                                return conteudo
                        else:
                            return await dinamicMarkdown(source, result.html)
                            
                    except Exception as e:
                        logging.error(f"CrawlScrapper não pode extrair o conteúdo. Detalhes: {e}")
                        return None
                else:

                    conteudo = await HandlerDinamic(url=source, source=result.html)
                    if conteudo:
                        return conteudo
            else:
                return await dinamicMarkdown(source)

    except Exception as e:
        logging.error(f"[Exceção] Um erro ocorreu durante o scraping de {source}. Detalhes: {e}")
        return None
    
async def dinamicMarkdown(url:str, source:str = None) -> str:
    """
    Converte o conteúdo de uma página da web ou uma fonte fornecida para o formato Markdown.

    Esta função pode processar o conteúdo de uma página HTML através de uma URL fornecida ou de uma fonte
    HTML diretamente fornecida como uma string. A função realiza os seguintes passos:
    
    1. Se uma fonte for fornecida (parâmetro `source`), ela será usada diretamente.
    2. Caso contrário, a função tenta buscar o conteúdo HTML da página na URL fornecida.
    3. Após obter o conteúdo HTML, a função o filtra e converte para Markdown.
    4. Se o processo for bem-sucedido, o conteúdo em Markdown é retornado.
    5. Caso contrário, um erro é registrado nos logs.

    Parâmetros:
    url (str): A URL da página web a ser processada. Necessário caso `source` não seja fornecido.
    source (str, opcional): Uma string contendo o código HTML a ser convertido. Se não fornecido, 
                            o conteúdo será recuperado a partir da URL fornecida.

    Retorna:
    str ou None: O conteúdo convertido para o formato Markdown ou `None` em caso de erro.

    Exceções:
    Nenhuma exceção explícita é levantada, mas erros no processamento do HTML ou na conversão
    para Markdown são registrados nos logs de erro.

    Exemplo:
    ```python
    markdown_content = await dinamicMarkdown('https://example.com')
    markdown_content = await dinamicMarkdown('https://example.com', '<html><body><p>Conteúdo</p></body></html>')
    ```

    Logs:
    A função registra erros no log se não for possível carregar a página ou realizar a conversão.
    """
    if source:
        result = source    
    else:
        result = getSource(url=url)
    if result:
        html_filtred = parseHTML(result)
        markdown = await to_markdown(html_filtred, url)
        if markdown:
            
            return markdown
        logging.error(f"Não foi possível carregar a página {url}.")
    else:
        logging.error(f"Não foi possível carregar a página {url}.")
        return None