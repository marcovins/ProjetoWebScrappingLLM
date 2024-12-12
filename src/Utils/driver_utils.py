from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
from src.Utils.imports import CHROME_DRIVER

def setup_driver():
    # Configurações do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--HEADLESS")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")  # User-Agent realista

    # Inicializar o driver com as opções
    service = Service(CHROME_DRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)


    # Script para desabilitar a detecção do WebDriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    return driver

# Função para adicionar atrasos aleatórios entre ações, simulando comportamento humano
def delay_action():
    time.sleep(random.uniform(1, 3))  # Atrasos entre 1 e 3 segundos