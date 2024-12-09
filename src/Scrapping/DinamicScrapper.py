from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from src.Utils.imports import MODEL_URL_REQUEST, PROMPT
import json
import re

def extract_pure_json(input_string: dict) -> dict:
    """
    Extrai o JSON válido de uma string, ignorando comentários e delimitadores.

    Args:
        input_string (str): String contendo o JSON e possíveis comentários.

    Returns:
        dict: O dicionário Python representando o JSON extraído.
    """
    try:
        
        # Regex para capturar qualquer JSON válido na string
        json_match = re.search(r"\{.*\}", input_string, re.DOTALL)
        if not json_match:
            raise ValueError("Nenhum JSON válido encontrado na string fornecida.")
        
        # Extrair o JSON bruto
        json_raw = json_match.group(0).strip()

        # Parse o JSON para garantir que é válido
        json_data = json.loads(json_raw)

        # Retorna o JSON como dicionário Python
        return json_data
    except:
        print("Refazendo request para melhorar resposta...")
        schema = {
        'descricao': "Descrição do texto",
        'tag': "Palavra que defina a área de conhecimento",
        'metadados': "Metadados adicionais presentes no texto",
        }

        requisicao = {
            "model": "llama3.2",
            "prompt": f"Retorne conforme esta estrutura json: {schema}\nDados do site:\n{input_string} ",
            "stream": False
        }

        response = requests.post(url=MODEL_URL_REQUEST, json=requisicao)
        response.raise_for_status()
        result = response.json().get('response', {})
        return result
        


# Configuração do Selenium
def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--disable-gpu")  # Melhor compatibilidade
    chrome_options.add_argument("--no-sandbox")  # Necessário em alguns ambientes
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas em contêineres
    
    service = Service('C:/Users/marcosbelo/Documents/WebScrapping/rsc/chromedriver-win32/chromedriver.exe')  # Substituir pelo caminho do ChromeDriver
    return webdriver.Chrome(service=service, options=chrome_options)

# Obter o HTML dinâmico com Selenium
def getSource(url: str) -> str:
    try:
        driver = setup_driver()
        driver.get(url)
        
        WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete")

        # Obter o HTML completo da página renderizada
        html = driver.page_source
        return html
    
    except Exception as e:
        print(f"Erro ao carregar a página: {e}")
        return None
    
    finally:
        driver.quit()

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

    # Extrair tags p
    p_tags = soup.find_all('p')
    data['p_tags'] = [tag.text for tag in p_tags]
    '''
    # Extrair links
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            links.append(href)
    data['links'] = links'''
    
    return data

# Enviar requisição para o modelo de LLM
def getResponse(prompt: str, data: dict):

    schema = {
        'descricao': "O texto gerado pela LLM",
        'tag': "Categoria do site (Saúde, Educação, Trabalho, Agropecuária, Minério, etc...)",
        'metadados': "Metadados adicionais retornados pelo modelo",
    }

    requisicao = {
        "model": "llama3.2",
        "prompt": f"{prompt}:\nRetorne conforme este schema: {schema}\nDados do site:\n{data} ",
        "stream": False
    }
    print(MODEL_URL_REQUEST)
    response = requests.post(url=MODEL_URL_REQUEST, json=requisicao)
    response.raise_for_status()
    return response.json().get('response', "Erro na resposta do modelo")

# Função principal para lidar com páginas dinâmicas
def HandlerDinamic(url: str, prompt: str = PROMPT):
    html = getSource(url)
    if html:
        data = parseHTML(html)
        if data:
            print("\nDATA:\n",data)
            # Responder ao prompt usando o modelo LLM
            response = getResponse(prompt, data)
            print(response)
            return extract_pure_json(response)
    return "Não foi possível carregar a página."
