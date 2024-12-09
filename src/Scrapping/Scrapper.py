from src.Utils.IU import tk
from scrapegraphai.graphs import SmartScraperGraph
from src.Schemas.ResponseSchema import ResponseSchema
from src.Scrapping.DinamicScrapper import HandlerDinamic
from src.Scrapping.CrawlScrapper import CrawlScrapper
import asyncio
from src.Utils.imports import PROMPT, GRAPH_CONFIG
import json

# Decodificador Unicode
def decode_unicode(text):
    try:
        return bytes(text, 'utf-8').decode('unicode_escape')
    except Exception:
        return text

# Atualizar widget de texto
def update_text_widget(widget, text):
    widget.delete(1.0, tk.END)
    widget.insert(tk.END, text)

# Função para scraping estático
def run_static_scraper(source, on_complete, output_widget1 = None):
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
def run_dynamic_scraper(source, on_complete, output_widget2 = None):
    try:
        result = HandlerDinamic(url=source, prompt=PROMPT)
        if output_widget2:
            output_widget2.after(0, lambda: update_text_widget(output_widget2, result))
        return result
    except Exception as e:
        print(f"Erro no scraper dinâmico: {type(e).__name__} - {str(e)}")
    finally:
        on_complete()

# Função para gerar o markdown
def generate_markdown_content(source, output_widget3 = None):
    try:
        result = asyncio.run(CrawlScrapper(source=source))
        if output_widget3:
            output_widget3.after(0, lambda: update_text_widget(output_widget3, result))
    except Exception as e:
        print(f"Erro na geração do markdown: {type(e).__name__} - {str(e)}")