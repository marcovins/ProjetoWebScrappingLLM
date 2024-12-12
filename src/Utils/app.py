from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from src.Scrapping.CrawlScrapper import CrawlScrapper
from src.Scrapping.DinamicScrapper import HandlerDinamic
from src.Utils.json_utils import limpar_json, texto_para_json
from src.Utils.http_utils import make_request_to_model
import logging

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="API de Scrapping",
    description="API for URL Scraping and Markdown Generation",
    version="0.0.1",
    debug=True
)

# Configuração de logging para diagnóstico
logging.basicConfig(level=logging.INFO)

# Modelo para entrada
class URLInput(BaseModel):
    url: HttpUrl

# Modelo para resposta
class ScrapeResponse(BaseModel):
    url: str
    result: dict  # Alterado para ser um dicionário em vez de uma string

class ErrorResponse(BaseModel):
    detail: str

@app.post("/scrape", response_model=ScrapeResponse, responses={500: {"model": ErrorResponse}})
async def scrape_dynamic(input: URLInput):
    """
    Realiza o scraping dinâmico de uma URL utilizando Selenium e BeautifulSoup.
    """
    try:
        logging.info("Iniciando scraping dinâmico para URL: %s", input.url)
        result = HandlerDinamic(str(input.url))
        
        if not result:
            logging.error("Resultado vazio ao processar a URL: %s", input.url)
            raise HTTPException(status_code=500, detail="Erro ao processar a URL")
        
        logging.info("Resultado do scraping recebido com sucesso.")
        print(result)
        # Limpeza do conteúdo JSON
        cleaned_result = limpar_json(result)
        logging.debug("Resultado limpo: %s", cleaned_result)
        
        # Verificar se result é um dicionário válido e tem a chave 'result'
        if isinstance(cleaned_result, dict) and 'result' in cleaned_result:
            cleaned_result = cleaned_result['result']
        else:
            logging.error("Erro ao processar o JSON. Chave 'result' não encontrada ou estrutura inválida.")
            raise HTTPException(status_code=500, detail="Erro ao processar o JSON.")
        
        return {"url": str(input.url), "result": cleaned_result}
    
    except Exception as e:
        logging.error("Erro ao realizar scraping para a URL %s: %s", input.url, str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao realizar scraping: {str(e)}")


@app.post("/generate-markdown", responses={500: {"model": ErrorResponse}})
async def generate_markdown(input: URLInput):
    """
    Gera o conteúdo Markdown de uma URL utilizando AsyncWebCrawler.
    """
    try:
        logging.info("Iniciando geração de Markdown para URL: %s", input.url)
        result = await CrawlScrapper(str(input.url))
        
        if not result:
            logging.error("Resultado vazio ao gerar markdown para a URL: %s", input.url)
            raise HTTPException(status_code=500, detail="Erro ao gerar o markdown")
        
        logging.info("Conteúdo recebido para Markdown com sucesso: %s", result)
        
        # Limpa o JSON retornado para a chave 'result' usando a função limpar_json
        logging.debug("Resultado limpo do Markdown: %s", result)
        
        return result
    
    except Exception as e:
        logging.error("Erro ao gerar markdown para a URL %s: %s", input.url, str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao gerar markdown: {str(e)}")


'''
@app.post("/generate-markdown-LLM", responses={500: {"model": ErrorResponse}})
async def generate_markdown_LLM(input: URLInput):
    """
    Gera o conteúdo Markdown de uma URL utilizando AsyncWebCrawler e processa com LLM.
    """
    try:
        logging.info("Iniciando geração de Markdown para URL: %s", input.url)
        
        # Etapa 1: Scraping da URL
        result = await CrawlScrapper(str(input.url))
        if not result:
            logging.error("Resultado vazio ao gerar markdown para a URL: %s", input.url)
            raise HTTPException(status_code=500, detail="Erro ao gerar o markdown")
        
        logging.info("Conteúdo recebido para Markdown com sucesso: %s", result)

        # Etapa 2: Processamento com LLM
        llm_response = make_request_to_model(
            #promptOpcional="Filtre as principais informações e me devolva como dicionario:",
            data=result
        )
        
        
        if not llm_response:
            logging.error("Resposta inválida ou nula do modelo LLM para a URL: %s", input.url)
            raise HTTPException(status_code=500, detail="Erro ao processar o conteúdo no modelo LLM")
        
        logging.info("Resposta do modelo LLM recebida: %s", llm_response)


        return {"url": str(input.url), "result": llm_response}

    except HTTPException as http_exc:
        # Rethrow HTTP exceptions para responder corretamente
        logging.error("HTTPException ao processar a URL %s: %s", input.url, str(http_exc))
        raise http_exc

    except Exception as e:
        # Captura erros gerais
        logging.error("Erro inesperado ao processar a URL %s: %s", input.url, str(e))
        raise HTTPException(status_code=500, detail=f"Erro ao gerar markdown: {str(e)}")
'''