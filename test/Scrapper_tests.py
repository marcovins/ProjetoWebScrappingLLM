import pytest
from src.Scrapping.DinamicScrapper import getSource, parseHTML

# Listas de URLs para testar
dynamic_sites = [
    "https://www.youtube.com",
    "https://www.airbnb.com",
    "https://www.google.com/maps",
    "https://www.netflix.com",
    "https://www.amazon.com/s?k=books",
    "https://app.powerbi.com",
    "https://www.cnnbrasil.com.br/economia/macroeconomia/industria-deve-ser-grande-destaque-do-pib-no-3o-trimestre-dizem-economistas/",
    "https://www.fiepb.com.br/",
    "https://medium.com/wise-well/the-surprising-unhealthy-filth-of-shopping-carts-a8a714a2c100",
]

static_sites = [
    "https://example.com",
    "https://en.wikipedia.org/wiki/Web_scraping",
    "https://www.gov.br",
    "https://www.w3.org",
    "https://docs.python.org/3/",
    "https://html5test.com"
]

@pytest.mark.parametrize("url", dynamic_sites + static_sites)
def test_get_source_valid(url):
    """
    Testar getSource com uma variedade de URLs dinâmicas e estáticas
    """
    html = getSource(url)
    assert html is not None, f"A função getSource não retornou HTML válido para {url}"

def test_get_source_invalid():
    """
    Testar getSource com uma URL inválida
    """
    url = "https://invalid-url.com"
    html = getSource(url)
    assert html is None, "A função getSource deveria retornar None para URL inválida"

def test_parse_html():
    """
    Testar parseHTML com HTML simples
    """
    html = """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="This is a test page.">
        </head>
        <body>
            <h1>Header 1</h1>
            <a href="https://link1.com">Link 1</a>
        </body>
    </html>
    """
    data = parseHTML(html)
    assert data['title'] == "Test Page", "O título da página não foi extraído corretamente"
    assert data['meta_description'] == "This is a test page.", "A meta descrição não foi extraída corretamente"
    assert "<html" in html.lower(), f"O HTML retornado por não contém a tag <html>"
    assert "</html>" in html.lower(), f"O HTML retornado não contém a tag </html>"
    assert html is not None, f"getSource não retornou nenhum HTML"
    #assert "https://link1.com" in data['links'], "Os links não foram extraídos corretamente"
