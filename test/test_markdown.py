from fastapi.testclient import TestClient
from src.Utils.app import app
from fastapi.testclient import TestClient  # Importando o TestClient da FastAPI

# Lista de URLs para testar
URLS_VALIDAS = [
    "https://books.toscrape.com/",
    "https://quotes.toscrape.com/",
    "https://jsonplaceholder.typicode.com/",
    "https://en.wikipedia.org/wiki/Main_Page",
    "https://www.imdb.com/pt/",
    "https://finance.yahoo.com/",
    "https://www.nationalgeographic.com/",
    "https://www.britannica.com/",
    "https://www.nobelprize.org/",
    "https://www.nationalgeographic.com/environment/article/mount-everest",
    "https://www.britannica.com/place/Mount-Everest",
    "https://finance.yahoo.com/",
    "https://openweathermap.org/",
    "https://data.gov/",
    "https://tradingeconomics.com/",
    "https://www.coingecko.com/",
    "https://jsonplaceholder.typicode.com/",
    "https://reqres.in/",
    "https://medium.com/@recogna.nlp/explorando-o-bode-o-mais-novo-llm-em-portugu%C3%AAs-cb97f52935db",
    "https://www.bbc.com/news",
    "https://www.cnnbrasil.com.br/"
]

URLS_INVALIDAS = [
    "https://urlinvalida1234567.com",
    "http://sitequeprovavelmentenexiste.org"
]

# Remova a marcação @pytest.mark.asyncio, pois o TestClient é síncrono
def test_generate_markdown_valid_urls():
    """
    Testa o endpoint '/generate-markdown' com URLs válidas.
    Verifica se o status é 200 e se o resultado contém um Markdown válido.
    """
    client = TestClient(app)  # Usando TestClient
    for url in URLS_VALIDAS:
        response = client.post("/generate-markdown", json={"url": url})  # Remova o await
        
        assert response.status_code == 200, f"Falha na URL: {url}"
        data = response.json()
        
        assert "result" in data, "Resposta não contém o campo 'result'."
        assert len(data["result"].strip()) > 0, f"Markdown vazio para URL: {url}"
        print(f"✅ Teste bem-sucedido para URL: {url}")

def test_generate_markdown_invalid_urls():
    """
    Testa o endpoint '/generate-markdown' com URLs inválidas.
    Verifica se o status é 500 e se o erro é tratado corretamente.
    """
    client = TestClient(app)  # Usando TestClient
    for url in URLS_INVALIDAS:
        response = client.post("/generate-markdown", json={"url": url})  # Remova o await
        
        assert response.status_code == 500, f"A URL inválida {url} não retornou status 500."
        data = response.json()
        assert "detail" in data, "Resposta não contém o campo 'detail'."
        print(f"✅ Erro tratado corretamente para URL inválida: {url}")

def test_generate_markdown_missing_url():
    """
    Testa o endpoint '/generate-markdown' com corpo JSON inválido (sem URL).
    Verifica se o status é 422 (Unprocessable Entity).
    """
    client = TestClient(app)  # Usando TestClient
    response = client.post("/generate-markdown", json={})  # Remova o await
    
    assert response.status_code == 422, "A ausência da URL deveria retornar status 422."
    print("✅ Teste bem-sucedido para JSON inválido (sem URL).")
