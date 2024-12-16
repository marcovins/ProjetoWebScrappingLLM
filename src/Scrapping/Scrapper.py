import asyncio
from src.Utils.IU import tk
from scrapegraphai.graphs import SmartScraperGraph
from src.Schemas.ResponseSchema import ResponseSchema
from src.Scrapping.DinamicScrapper import HandlerDinamic
from src.Scrapping.CrawlScrapper import CrawlScrapper
from src.Utils.json_utils import limpar_json
from src.Utils.imports import PROMPT, GRAPH_CONFIG
import json

# Decodificador Unicode
def decode_unicode(text) -> str:
    """
    Decodifica string para o formato 'utf-8'

    Args:
        text (str): URL a ser processada.

    Returns:
        str: Texto decodificado para o formato 'utf-8'.
    """
    try:
        return bytes(text, 'utf-8').decode('unicode_escape')
    except Exception:
        return text

# Atualizar widget de texto
def update_text_widget(widget, text) -> None:
    """
    Atualiza o conteúdo de um widget de texto.
    
    Args:
        widget (tk.Text): Widget de texto.
        text (str): Texto a ser inserido no widget.

    Returns:
        None
    """
    widget.delete(1.0, tk.END)
    widget.insert(tk.END, text)

# Função para scraping estático
def run_static_scraper(source, on_complete, output_widget1:tk.Text = None) -> None:
    """
    Realiza scraping estático de uma URL utilizando a biblioteca SmartScraperGraph.
    Exibe no Widget da interface o resultado do scrapping.

    Args:
        url (str): URL a ser processada.
        on_complete (function): Função chamada após o scraping ser concluído.
        output_widget1 (tk.Text): Widget de texto para mostrar o resultado.

    Returns:
        None
    """
    try:
        smart_scraper_graph = SmartScraperGraph(
            prompt=PROMPT,
            source=source,
            config=GRAPH_CONFIG,
            schema=ResponseSchema,
        )
        result = smart_scraper_graph.run()
        if isinstance(result, dict) and len(result.keys()) > 4:
            decoded_result = decode_unicode(json.dumps(result, indent=4))
            if output_widget1:
                output_widget1.after(0, lambda: update_text_widget(output_widget1, decoded_result))
        else:
            if output_widget1:
                output_widget1.after(0, lambda: update_text_widget(output_widget1, "A página só pode ser carregada Dinamicamente..."))
    except Exception as e:
        print(f"Erro no scraper estático: {type(e).__name__} - {str(e)}")
    finally:
        on_complete()

# Função para scraping dinâmico
def run_dynamic_scraper(url: str, on_complete, output_widget2:tk.Text = None) -> None:
    """
    Realiza scraping dinâmico de uma URL utilizando as bibliotecas Selenium e BeautifulSoup.
    Exibe no Widget da interface o resultado do scrapping.

    Args:
        url (str): URL a ser processada.
        on_complete (function): Função chamada após o scraping ser concluído.
        output_widget2 (tk.Text): Widget de texto para mostrar o resultado.

    Returns:
        None
    """
    try:
        result = limpar_json(HandlerDinamic(url=url, prompt=PROMPT))
        if output_widget2:
            output_widget2.after(0, lambda: update_text_widget(output_widget2, result))
        return result
    except Exception as e:
        print(f"Erro no scraper dinâmico: {type(e).__name__} - {str(e)}")
    finally:
        on_complete()

def generate_markdown_content(url:str, output_widget3:tk.Text = None) -> None:
    """
    Gera o conteúdo Markdown de uma URL utilizando o scraper dinâmico.
    Exibe no Widget da interface o resultado do markdown.

    Args:
        url (str): URL a ser processada.
        output_widget3 (tk.Text): Widget de texto para mostrar o resultado.
    
    Returns:
        None
    """
    try:
        result = asyncio.run(CrawlScrapper(source=source))
        if output_widget3:
            output_widget3.after(0, lambda: update_text_widget(output_widget3, result))
    except Exception as e:
        print(f"Erro na geração do markdown: {type(e).__name__} - {str(e)}")