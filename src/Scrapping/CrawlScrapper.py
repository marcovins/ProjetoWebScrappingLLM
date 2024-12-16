import asyncio
from crawl4ai import AsyncWebCrawler
from src.Utils.imports import logging
async def CrawlScrapper(source: str, verbose: bool = False, timeout: int = 30 , markdown:bool = False) -> dict | None:
    """
    Realiza o scraping dinâmico de uma página da web usando a biblioteca AsyncWebCrawler do crawl4ai.

    Args:
        source (str): URL da página a ser acessada. Deve começar com 'http://' ou 'https://'.
        verbose (bool, opcional): Define se os logs detalhados devem ser exibidos durante a execução. 
            Padrão é False.
        timeout (int, opcional): Tempo limite para a operação em segundos. Padrão é 30.
        markdown (bool, opcional): Indica se o resultado deve ser processado e retornado em formato Markdown.
            Se False, retorna o resultado completo do scraping. Padrão é False.

    Returns:
        dict | None: 
            - Se `markdown` for True: Retorna o conteúdo da página em formato Markdown.
            - Se `markdown` for False: Retorna um dicionário com informações detalhadas do scraping, 
              incluindo o HTML e outros metadados.
            - None: Se ocorrer um erro durante o processamento.

    Raises:
        ValueError: Caso o argumento `source` não seja uma string ou não comece com 'http://' ou 'https://'.
        Exception: Caso ocorra um erro inesperado durante a operação de scraping.

    Exemplo:
        ```python
        result = asyncio.run(CrawlScrapper(source="https://www.example.com", markdown=True))
        print(result)
        ```
    """
    if not isinstance(source, str) or not source.startswith(("http://", "https://")):
        breakpoint()
        raise ValueError("A URL fornecida é inválida. Certifique-se de que começa com 'http://' ou 'https://'.")
    
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
                        '''
                        # Salvar em um arquivo
                        with open(f"rsc/Scraps/{source.replace("/", "").replace("https:", "")}.md", "w", encoding="utf-8") as arquivo:
                            arquivo.write(conteudo)
                            
                            print("Scraping concluído com sucesso!")
                            '''
                        return conteudo
                    except Exception as e:
                        logging.Error(f"CrawlScrapper não pode extrair o conteúdo. Detalhes: {e}")
                        return None
                else:
                    return result

    except Exception as e:
        logging.Error(f"[Exceção] Um erro ocorreu durante o scraping de {source}. Detalhes: {e}")
        return None
