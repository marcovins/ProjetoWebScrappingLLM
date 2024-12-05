import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
from threading import Thread
from dotenv import load_dotenv
import os
from scrapegraphai.graphs import SmartScraperGraph
from src.Schemas.ResponseSchema import ResponseSchema
from src.Scrapping.DinamicScrapper import HandlerDinamic

# Carregar variáveis de ambiente
load_dotenv()
MODEL_URL = os.getenv("MODEL_URL")
PROMPT = os.getenv("PROMPT")

if not MODEL_URL or not PROMPT:
    raise EnvironmentError("As variáveis de ambiente MODEL_URL e PROMPT não foram configuradas corretamente.")

GRAPH_CONFIG = {
    "llm": {
        "model": "llama3.2",
        "temperature": 0,
        "format": "json",
        "base_url": MODEL_URL,
    },
    "embeddings": {
        "model": "nomic-embed-text",
        "base_url": MODEL_URL,
    },
    "headless": True,
    "verbose": False,
}

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
def run_static_scraper(source, output_widget1, on_complete):
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
            output_widget1.after(0, lambda: update_text_widget(output_widget1, decoded_result))
        else:
            output_widget1.after(0, lambda: update_text_widget(output_widget1, "A página só pode ser carregada Dinamicamente..."))
    except Exception as e:
        print(f"Erro no scraper estático: {type(e).__name__} - {str(e)}")
    finally:
        on_complete()

# Função para scraping dinâmico
def run_dynamic_scraper(source, output_widget2, on_complete):
    try:
        result = HandlerDinamic(url=source, prompt=PROMPT)
        output_widget2.after(0, lambda: update_text_widget(output_widget2, result))
    except Exception as e:
        print(f"Erro no scraper dinâmico: {type(e).__name__} - {str(e)}")
    finally:
        on_complete()

# Interface gráfica
def start_gui():
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("1000x600")

    tk.Label(root, text="Insira a URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=100)
    url_entry.pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Resultado Busca Estática (Scrapegraphai):").grid(row=0, column=0, padx=20, pady=5)
    output_text1 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    output_text1.grid(row=1, column=0, padx=20, pady=5)

    tk.Label(frame, text="Resultado Busca Dinâmica (Selenium, BeautifulSoup):").grid(row=0, column=1, padx=20, pady=5)
    output_text2 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    output_text2.grid(row=1, column=1, padx=20, pady=5)

    # Variável para contar threads concluídas
    threads_completed = [0]

    # Callback quando uma thread é concluída
    def thread_done():
        threads_completed[0] += 1
        if threads_completed[0] == 2:  # Ambas as threads concluíram
            execute_button.config(state=tk.NORMAL)

    def execute_scraper():
        source = url_entry.get().strip()
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            threads_completed[0] = 0  # Resetar contador de threads
            execute_button.config(state=tk.DISABLED)  # Desativar o botão
            Thread(target=run_static_scraper, args=(source, output_text1, thread_done)).start()
            Thread(target=run_dynamic_scraper, args=(source, output_text2, thread_done)).start()

    execute_button = tk.Button(root, text="Executar Scraper", command=execute_scraper)
    execute_button.pack(pady=20)

    root.mainloop()