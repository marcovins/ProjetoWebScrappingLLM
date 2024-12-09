import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
MODEL_URL = os.getenv("MODEL_URL")
PROMPT = os.getenv("PROMPT")
MODEL_URL_REQUEST = os.getenv("MODEL_URL_REQUEST")

if not MODEL_URL or not PROMPT or not MODEL_URL_REQUEST:
    raise EnvironmentError("A variável de ambiente MODEL_URL não foi configurada corretamente.")

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