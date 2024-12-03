import json
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
    "headless": False,
    "verbose": False,
}

# Configuração da interface gráfica
def start_gui():
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("600x400")

    # Configuração de entrada e saída
    tk.Label(root, text="Insira a URL:").pack(pady=5)
    url_entry = tk.Entry(root, width=80)
    url_entry.pack(pady=5)

    tk.Label(root, text="Resultado:").pack(pady=5)
    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
    output_text.pack(pady=5)

    # Função para executar o scraper
    def execute_scraper():
        source = url_entry.get().strip()
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            run_scraper(source, output_text)

    tk.Button(root, text="Executar Scraper", command=execute_scraper).pack(pady=10)
    root.mainloop()

# Função principal para scraping
def run_scraper(source: str, output_widget: scrolledtext.ScrolledText):
    try:
        # Verificando a conexão de rede
        try:
            response = requests.head(source, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao verificar a conexão de rede:\n{e}")
            return

        prompt = "Me retorne uma raspagem de informações da seguinte página web"
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=GRAPH_CONFIG,
            schema=ResponseSchema,
        )

        # Executando o scraper
        result = smart_scraper_graph.run()
        if isinstance(result, dict) and result.get('tag') and result['tag'] != 'NA':
            print(f"Resultado obtido do SmartScraperGraph: {result['tag']}")
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, json.dumps(result, indent=4))
        else:
            print("Resultado vazio ou inadequado. Usando HandlerDinamic.")
            handle_dynamic(source, prompt, output_widget)

    except Exception as e:
        print(f"Erro ao executar o scraper principal: {type(e).__name__} - {str(e)}")
        messagebox.showerror("Erro no Scraper", f"Erro ao executar o scraper:\n{type(e).__name__} - {str(e)}")

# Função de fallback para scraping dinâmico
def handle_dynamic(source: str, prompt: str, output_widget: scrolledtext.ScrolledText):
    try:
        print(f"Chamando HandlerDinamic com URL={source} e prompt={prompt}")
        result = HandlerDinamic(url=source, prompt=prompt)
        output_widget.delete(1.0, tk.END)
        output_widget.insert(tk.END, result)
    except Exception as e:
        print(f"Erro ao executar o HandlerDinamic: {type(e).__name__} - {str(e)}")
        messagebox.showerror("Erro no Scraper Dinâmico", f"Erro ao executar o scraper dinâmico:\n{type(e).__name__} - {str(e)}")
