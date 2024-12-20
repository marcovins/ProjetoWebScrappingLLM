import aiofiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl
from src.Scrapping.CrawlScrapper import CrawlScrapper
from src.Scrapping.DinamicScrapper import HandlerDinamic, StaticScrapper, getSource, to_markdown
from src.Utils.http_utils import validar_resposta
from src.Utils.imports import FRONT
import logging
import asyncio

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="API de Scrapping",
    description="API for URL Scraping and Markdown Generation",
    version="0.0.1",
    debug=True
)

# Configuração de logging para diagnóstico
logging.basicConfig(level=logging.INFO)

# Modelos
class URLInput(BaseModel):
    url: HttpUrl

class ScrapeResponse(BaseModel):
    url: str
    result: dict

class MarkdownResponse(BaseModel):
    url: str
    markdown: str

class ErrorResponse(BaseModel):
    detail: str

@app.get("/", response_class=HTMLResponse)
async def root():
    async with aiofiles.open(FRONT, "r", encoding="utf-8") as file:
        html_content = await file.read()  # Lê o conteúdo do arquivo
    return HTMLResponse(content=html_content)

@app.post("/scrape", responses={500: {"model": ErrorResponse}})
async def scrape_dynamic(input: URLInput):
    """
    Executa o scraping dinâmico ou estático em uma URL fornecida, tentando diversas abordagens 
    de scraping para obter o conteúdo da página.

    A função tenta realizar o scraping de uma URL fornecida utilizando três abordagens diferentes:
    1. **Scraping Dinâmico com `CrawlScrapper`**: Utiliza o crawler assíncrono.
    2. **Scraping Estático com `StaticScrapper`**: Usa o SmartScraperGraph.
    3. **Scraping Dinâmico com `HandlerDinamic`**: Usa Selenium e BeautifulSoup.

    Caso uma dessas abordagens seja bem-sucedida, ela retorna os dados extraídos. Se nenhuma abordagem 
    resultar em dados válidos, a função lança um erro HTTP 500.

    ### Parâmetros:
    - **input**: Objeto contendo a URL a ser processada.
        - **url** (str): A URL da qual o conteúdo será extraído.

    ### Respostas:
    - **200 OK**: Retorna a URL e o conteúdo extraído da página.
    - **500 Internal Server Error**: Caso nenhum scraping seja bem-sucedido.

    ### Exemplo de Uso:
    Envie a URL da página que deseja realizar o scraping:

    ```json
    {
        "url": "https://www.exemplo.com"
    }
    ```

    **Resposta de Sucesso**:
    ```json
    {
        "url": "https://www.exemplo.com",
        "result": { ...conteúdo extraído... }
    }
    ```

    **Resposta de Erro**:
    Caso o scraping falhe, você receberá:
    ```json
    {
        "detail": "Erro ao realizar scraping"
    }
    ```

    ### Exceções:
    - **HTTPException (500)**: Se todas as abordagens de scraping falharem ou ocorrerem erros inesperados.

    """
    try:

        logging.info("Iniciando scraping dinâmico para URL: %s", input.url)
        result = await HandlerDinamic(str(input.url))
        if result:
            return result
        
        logging.warning("Resultado vazio para scraping dinâmico, tentando scraping estático.")
        result = await StaticScrapper(str(input.url))
        if result:
            return result

        logging.warning("Scraping estático falhou, tentando CrawlScrapper.")
        result = await CrawlScrapper(str(input.url))
        if result:
            return result
               
        logging.error("Nenhuma abordagem de scraping retornou resultado válido.")
        raise HTTPException(status_code=500, detail="Erro ao realizar scraping")
    except Exception as e:
        logging.exception("Erro inesperado ao realizar scraping para a URL: %s", input.url)
        raise HTTPException(status_code=500, detail=f"Erro ao realizar scraping: {str(e)}")

@app.post("/generate-markdown",response_model=MarkdownResponse, responses={500: {"model": ErrorResponse}})
async def generate_markdown(input: URLInput):
    """
    Esta função recebe uma URL, realiza o scraping dinâmico da página e converte o conteúdo para o formato Markdown.  
    Caso o processo seja bem-sucedido, retorna a URL e o conteúdo gerado.

    1. O parâmetro `input` contém a URL fornecida.
    2. A função tenta gerar o conteúdo em Markdown utilizando a função `CrawlScraper`.
    3. Se o scraping for bem-sucedido, retorna o conteúdo gerado em Markdown.
    4. Caso ocorra algum erro, é levantada uma exceção HTTP com o código apropriado.

    Caso uma dessas abordagens seja bem-sucedida, ela retorna os dados extraídos. Se nenhuma abordagem 
    resultar em dados válidos, a função lança um erro HTTP 500.

    - **input**: Objeto contendo a URL a ser processada.
        - **url** (str): A URL da qual o conteúdo será extraído.

    ### Respostas:
    - **200 OK**: Um dicionário contendo:
      - **url**: A URL processada.
      - **result**: O conteúdo da página convertido para o formato Markdown.
    - **422 Unprocessable Entity**: Caso a URL fornecida seja inválida.
    - **500 Internal Server Error**: Caso ocorra um erro interno durante o processamento.

    ### Exemplo de Uso:
    Envie a URL da página que deseja gerar o markdown:

    ```json
    {
      "url": "https://www.exemplo.com"
    }
    ```

    **Resposta de Sucesso**:
    ```json
    {
        "url": "https://www.exemplo.com",
        "markdown": { ...markdown gerado... }
    }
    ```

    **Resposta de Erro**:
    Caso o scraping falhe, você receberá:
    ```json
    {
        "detail": "Erro ao realizar scraping"
    }
    ```

    ### Exceções:
    - **422 Unprocessable Entity**: Caso a URL fornecida seja inválida.
    - **500 Internal Server Error**: Caso ocorra um erro interno durante o processamento.

    
    """

    logging.info("Iniciando geração de Markdown para URL: %s", input.url)

    try:
        # Executa o scraping usando a função CrawlScrapper
        result = await CrawlScrapper(str(input.url), markdown=True)

        # Log para depuração
        logging.info(f"Resultado recebido: {result}")

        if isinstance(result, str):  # Se `result` já é uma string de Markdown
            logging.info("Markdown gerado com sucesso.")
            return {"url": str(input.url), "markdown": result}
        # Caso o retorno não seja válido
        logging.error("O resultado do scraping é inválido ou está vazio.")
        raise HTTPException(status_code=500, detail="Não foi possível processar o conteúdo da página.")

    except Exception as e:
        logging.error(f"Erro ao gerar markdown: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao tentar gerar o Markdown.")