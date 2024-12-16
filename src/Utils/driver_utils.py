from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from src.Utils.imports import CHROME_DRIVER

def setup_driver():
    """
    Configura e retorna uma instância do driver Selenium para automação do navegador.

    Returns:
        webdriver.Chrome: Instância configurada do driver Selenium.

    Raises:
        Exception: Caso a configuração do driver falhe.
    """
    # Configurações do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--HEADLESS")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")  # User-Agent realista
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-webgl')

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