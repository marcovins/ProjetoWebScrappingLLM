import os
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
MODEL_URL = os.getenv("MODEL_URL")
PROMPT = os.getenv("PROMPT")
MODEL_URL_REQUEST = os.getenv("MODEL_URL_REQUEST")
CHROME_DRIVER = os.getenv("CHROME_DRIVER")
COOKIES = os.getenv("COOKIES")

if not MODEL_URL or not PROMPT or not MODEL_URL_REQUEST or not CHROME_DRIVER or not COOKIES:
    raise EnvironmentError("As variáveis de ambiente não foram configuradas corretamente.")

GRAPH_CONFIG = {
    "llm": {
        "model": "llama3.2",
        "temperature": 0,
        "format": "json",
        "base_url": MODEL_URL,
    },
    "embeddings": {
        "model": "nomic-embed-text",
        "base_url": MODEL_URL,
    },
    "headless": True,
    "verbose": False,
}

schema = {
        'descricao': "Descrição do texto",
        'tag': "Categoria do site",
        'metadados': "Metadados adicionais",
        'descricao completa': "Detalhamento do que é entendido"
        }

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
