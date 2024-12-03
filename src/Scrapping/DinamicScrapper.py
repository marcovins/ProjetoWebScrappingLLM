from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do modelo LLM
MODEL_URL = os.getenv("MODEL_URL_REQUEST")

# Configuração do Selenium
def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--disable-gpu")  # Melhor compatibilidade
    chrome_options.add_argument("--no-sandbox")  # Necessário em alguns ambientes
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas em contêineres
    
    service = Service('path/to/chromedriver')  # Substituir pelo caminho do ChromeDriver
    return webdriver.Chrome(service=service, options=chrome_options)

# Obter o HTML dinâmico com Selenium
def getSource(url: str) -> str:
    try:
        driver = setup_driver()
        driver.get(url)
        
        # Aguarda até que o corpo da página seja carregado
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Obter o HTML completo da página renderizada
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"Erro ao carregar a página: {e}")
        return None

# Parsear o HTML usando BeautifulSoup
def parseHTML(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
    
    # Extrair o título
    title = soup.find('title')
    data['title'] = title.text if title else "Sem título"
    
    # Extrair meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    data['meta_description'] = meta_desc['content'] if meta_desc else "Sem descrição"
    
    # Extrair tags h1
    h1_tags = soup.find_all('h1')
    data['h1_tags'] = [tag.text for tag in h1_tags]
    
    # Extrair links
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    data['links'] = links
    
    return data

# Enviar requisição para o modelo de LLM
def getResponse(prompt: str, data: dict):
    requisicao = {
        "model": "llama3.2",
        "prompt": f"{prompt}:\n{data}",
        "stream": False
    }

    response = requests.post(MODEL_URL, json=requisicao)
    response.raise_for_status()
    
    return response.json().get('response', "Erro na resposta do modelo")

# Função principal para lidar com páginas dinâmicas
def HandlerDinamic(url: str, prompt: str):
    html = getSource(url)
    if html:
        data = parseHTML(html)
        if data:
            # Responder ao prompt usando o modelo LLM
            response = getResponse(prompt, data)
            return response
    return "Não foi possível carregar a página."
