import json
import re
import time
from scrapegraphai.graphs import SmartScraperGraph
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext
from src.Schemas.ResponseSchema import ResponseSchema
from src.Scrapping.DinamicScrapper import HandlerDinamic
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do modelo LLM
MODEL_URL = os.getenv("MODEL_URL")
PROMPT = os.getenv("PROMPT")

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

# Configuração da interface gráfica
def start_gui():
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("1000x600")  # Ajuste do tamanho da janela

    # Configuração de entrada para URL
    tk.Label(root, text="Insira a URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=100)
    url_entry.pack(pady=5)

    # Frame para as caixas de texto lado a lado
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Adicionando a primeira Label e a primeira caixa de texto (Resultado Busca Estática)
    tk.Label(frame, text="Resultado Busca Estática(Scrapegraphai):").grid(row=0, column=0, padx=20, pady=5)
    output_text1 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    output_text1.grid(row=1, column=0, padx=20, pady=5)

    # Adicionando a segunda Label e a segunda caixa de texto (Resultado Busca Dinâmica)
    tk.Label(frame, text="Resultado Busca Dinâmica(Selenium, BeatifulSoup):").grid(row=0, column=1, padx=20, pady=5)
    output_text2 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    output_text2.grid(row=1, column=1, padx=20, pady=5)

    # Função para executar o scraper
    def execute_scraper():
        source = url_entry.get().strip()
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            run_scraper(source, output_text1,output_text2 )  # Chama a função de scraping para a primeira caixa de texto

    # Botão para executar o scraper
    execute_button = tk.Button(root, text="Executar Scraper", command=execute_scraper)
    execute_button.pack(pady=20)

    root.mainloop()

# Função principal para scraping
def run_scraper(source: str, output_widget1: scrolledtext.ScrolledText, output_widget2: scrolledtext.ScrolledText):
    try:
        # Verificando a conexão de rede
        try:
            response = requests.head(source, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao verificar a conexão de rede:\n{e}")
            return

        prompt = PROMPT
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=GRAPH_CONFIG,
            schema=ResponseSchema,
        )

        # Executando o scraper
        result = smart_scraper_graph.run()
        if isinstance(result, dict) and len(result.keys()) > 4:
            print(f"Resultado obtido do SmartScraperGraph: {result}")
            # Decodificando caracteres Unicode
            decoded_result = decode_unicode(json.dumps(result, indent=4))
            output_widget1.delete(1.0, tk.END)
            output_widget1.insert(tk.END, decoded_result)
        else:
            output_widget1.delete(1.0, tk.END)
            output_widget1.insert(tk.END, "A página só pode ser carregada Dinamicamente...")
        handle_dynamic(source, prompt, output_widget2)
        

    except Exception as e:
        print(f"Erro ao executar o scraper principal: {type(e).__name__} - {str(e)}")
        messagebox.showerror("Erro no Scraper", f"Erro ao executar o scraper:\n{type(e).__name__} - {str(e)}")

# Função de fallback para scraping dinâmico
def handle_dynamic(source: str, prompt: str, output_widget: scrolledtext.ScrolledText):
    try:
        print(f"Chamando HandlerDinamic com URL={source} e prompt={prompt}")
        result = HandlerDinamic(url=source, prompt=prompt)
        # Decodificando caracteres Unicode
        decoded_result = decode_unicode(result)
        output_widget.delete(1.0, tk.END)
        output_widget.insert(tk.END, result)
    except Exception as e:
        print(f"Erro ao executar o HandlerDinamic: {type(e).__name__} - {str(e)}")
        messagebox.showerror("Erro no Scraper Dinâmico", f"Erro ao executar o scraper dinâmico:\n{type(e).__name__} - {str(e)}")

# Função para decodificar os caracteres Unicode
def decode_unicode(text):
    # Utiliza a decodificação com 'unicode_escape'
    decoded_text = bytes(text, 'utf-8').decode('unicode_escape')
    return decoded_text

start_gui()
time.sleep(2)
exit(0)