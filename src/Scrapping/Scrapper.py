import tkinter as tk
from src.Schemas.ResponseSchema import ResponseSchema
from src.Scrapping.DinamicScrapper import HandlerDinamic
from src.Scrapping.CrawlScrapper import CrawlScrapper
from src.Utils.json_utils import limpar_json
from src.Utils.imports import PROMPT, GRAPH_CONFIG
import json
import requests
from bs4 import BeautifulSoup

# Decodificador Unicode
def decode_unicode(text) -> str:
    try:
        return bytes(text, 'utf-8').decode('unicode_escape')
    except Exception:
        return text

# Atualizar widget de texto
def update_text_widget(widget, text) -> None:
    widget.delete(1.0, tk.END)
    widget.insert(tk.END, text)

# Função para scraping dinâmico
async def run_dynamic_scraper(url: str, output_widget1: tk.Text = None) -> None:
    try:
        result = await HandlerDinamic(url=url, prompt=PROMPT)
        if output_widget1:
            output_widget1.after(0, lambda: update_text_widget(output_widget1, result))
        return result
    except Exception as e:
        print(f"Erro no scraper dinâmico: {type(e).__name__} - {str(e)}")

# Função assíncrona para gerar conteúdo em Markdown
async def generate_markdown_content(url: str, output_widget2: tk.Text = None) -> None:
    """
    Gera o conteúdo Markdown de uma URL utilizando o scraper dinâmico.
    Exibe no Widget da interface o resultado do markdown.

    Args:
        url (str): URL a ser processada.
        output_widget2 (tk.Text): Widget de texto para mostrar o resultado.

    Returns:
        None
    """
    try:
        result = await CrawlScrapper(source=url, markdown=True)
        if output_widget2:
            output_widget2.after(0, lambda: update_text_widget(output_widget2, result))
    except Exception as e:
        print(f"Erro na geração do markdown: {type(e).__name__} - {str(e)}")