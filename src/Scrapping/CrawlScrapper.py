from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from src.Schemas import ResponseSchema
from dotenv import load_dotenv
import asyncio
import os
import requests

# Carregar variáveis de ambiente
load_dotenv()
MODEL_URL = os.getenv("MODEL_URL")
MODEL_REQUEST_URL = os.getenv("MODEL_REQUEST_URL")
PROMPT = os.getenv("PROMPT")

if not MODEL_URL or not PROMPT:
    raise EnvironmentError("As variáveis de ambiente MODEL_URL e PROMPT não foram configuradas corretamente.")


def filterOut(data:str):

    requisicao = {
        "model": "llama3.2",
        "prompt": f"Filtre esse scrapping:\n{data} ",
        "stream": False
    }
    print(MODEL_REQUEST_URL)
    response = requests.post(url=MODEL_REQUEST_URL, json=requisicao)
    response.raise_for_status()
    return response.json().get('response', "Erro na resposta do modelo")

async def CrawlScrapper(source: str, verbose: bool = False, timeout: int = 30):
    """
    Realiza scraping assíncrono de uma URL usando AsyncWebCrawler.

    Args:
        source (str): URL da página a ser scrapeada.
        verbose (bool): Ativa logs detalhados se True.
        timeout (int): Tempo limite para a operação (em segundos).

    Returns:
        dict: Resultado do scraping em caso de sucesso.
        None: Caso ocorra falha, retorna None.
    """
    if not isinstance(source, str) or not source.startswith(("http://", "https://")):
        raise ValueError("A URL fornecida é inválida. Certifique-se de que começa com 'http://' ou 'https://'.")
    
    try:
        # Criar a instância do crawler corretamente com o parâmetro verbose
        async with AsyncWebCrawler(verbose=verbose) as crawler:
            # Ações JavaScript para esperar e carregar o conteúdo

            result = await crawler.arun(
                url=source,
                # Configurações básicas
                exclude_external_links=True,
                fit_markdown=True,

                # Parâmetros opcionais para testar
                word_count_threshold=5,
                excluded_tags=['form', 'header'],
                process_iframes=True,
                remove_overlay_elements=True,
                extraction_strategy=LLMExtractionStrategy(
                provider="ollama/llama3.2",
                schema=ResponseSchema,
                instruction=PROMPT,
                base_url=MODEL_URL,
                extraction_type="schema",
                ),

                # Cache e timeout
                bypass_cache=False,
                timeout=30,
                delay_before_return_html=3.0,  # Aguardar mais tempo antes de capturar o HTML

            )
            if result:
                # Conteúdo da variável
                conteudo = result.markdown

                # Salvar em um arquivo
                with open(f"rsc/Scraps/{source.replace("/", "").replace("https:", "")}.md", "w", encoding="utf-8") as arquivo:
                    arquivo.write(conteudo)
                    
                    print("Scraping concluído com sucesso!")
                    print(result.markdown)
                    return result
            else:
                print("Falha ao extrair o conteúdo.")

    except Exception as e:
        print(f"[Exceção] Um erro ocorreu durante o scraping de {source}. Detalhes: {e}")
        return None

asyncio.run(CrawlScrapper("https://app.powerbi.com/view?r=eyJrIjoiNWMxZTNkYjItNmFmZS00NTNhLTlmZTgtY2I4OGY3ZDhmNjAzIiwidCI6ImI4YzI1OTMyLTVlNzYtNGIyYi05YzUzLWQ0MTc0NWU5YzkyZCJ9"))