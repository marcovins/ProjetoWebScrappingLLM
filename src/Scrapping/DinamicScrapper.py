from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from src.Utils.http_utils import make_request_to_model
from src.Utils.imports import PROMPT, logging
from src.Utils.driver_utils import setup_driver

def getSource(url: str) -> str:
    driver = None
    try:
        driver = setup_driver()
        driver.get(url)
        
        # Espera até que a página carregue completamente
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )


        return driver.page_source
    except Exception as e:
        logging.error(f"Erro ao carregar a página {url}: {e}")
        return None
    finally:
        if driver:
            driver.quit()


# Parse HTML com BeautifulSoup
def parseHTML(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'title': soup.find('title').text if soup.find('title') else "Sem título",
        'meta_description': soup.find('meta', attrs={'name': 'description'}),
        'h1_tags': [tag.text for tag in soup.find_all('h1')],
        'p_tags': [tag.text for tag in soup.find_all('p')],
    }
    return data

def HandlerDinamic(url: str, prompt: str = PROMPT):
    html = getSource(url)
    if html:
        data = parseHTML(html)
        
        response = make_request_to_model(data)
        return response
    return "Não foi possível carregar a página."

