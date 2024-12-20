import os
import logging
from dotenv import load_dotenv

"""
Configurações iniciais do sistema, carregando variáveis de ambiente e configurando parâmetros 
necessários para a execução das funções de scraping, comunicação com o modelo e outros processos.

Este módulo realiza a carga das variáveis de ambiente a partir de um arquivo `.env`, garantindo que 
todas as configurações necessárias sejam carregadas corretamente para a execução do programa. Além 
disso, define as configurações do modelo, como o modelo de linguagem a ser utilizado e o modelo de 
embedding, além de configurar o logger para rastrear o fluxo do sistema.

Variáveis de Ambiente Carregadas:
    - MODEL_URL: URL base do modelo de linguagem.
    - PROMPT: Prompt utilizado como entrada para o modelo.
    - MODEL_URL_REQUEST: URL utilizada para fazer requisições ao modelo.
    - CHROME_DRIVER: Caminho para o driver do Chrome utilizado pelo Selenium.
    - COOKIES: Caminho do diretório onde os cookies serão armazenados.
    - SCRAPS: Caminho do diretório onde os scraps em formato Markdown serão armazenados.

Configuração do Modelo:
    - `GRAPH_CONFIG`: Dicionário com as configurações do modelo de linguagem (`llama3.2`) e o modelo de 
      embeddings (`nomic-embed-text`), além de opções como `headless` e `verbose`.

Configuração do Logger:
    - O logger está configurado para mostrar mensagens de log em nível de `INFO` no formato: 
      `data/hora - nível - mensagem`.

Exceção:
    - Se alguma das variáveis de ambiente não estiver configurada corretamente, será levantada uma exceção 
      `EnvironmentError` com a mensagem: "As variáveis de ambiente não foram configuradas corretamente.".

Exemplo:
    O módulo é executado automaticamente ao ser importado, carregando as variáveis de ambiente e configurando 
    o sistema. Não requer chamada explícita de funções para configuração inicial.
"""

# Carregar variáveis de ambiente
load_dotenv()
MODEL_URL = os.getenv("MODEL_URL")
PROMPT = os.getenv("PROMPT")
MODEL_URL_REQUEST = os.getenv("MODEL_URL_REQUEST")
CHROME_DRIVER = os.getenv("CHROME_DRIVER")
COOKIES = os.getenv("COOKIES")
SCRAPS = os.getenv("SCRAPS")
FRONT = os.getenv("FRONT")

if not MODEL_URL or not PROMPT or not MODEL_URL_REQUEST or not CHROME_DRIVER or not COOKIES or not SCRAPS or not FRONT:
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
