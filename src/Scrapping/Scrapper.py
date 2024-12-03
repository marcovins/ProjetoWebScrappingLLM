import json  # Import necessário para manipular JSON
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
    # Inicialização da janela principal
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("600x400")

    # Label e campo de entrada para URL
    url_label = tk.Label(root, text="Insira a URL:")
    url_label.pack(pady=5)

    url_entry = tk.Entry(root, width=80)
    url_entry.pack(pady=5)

    # Texto para saída
    output_label = tk.Label(root, text="Resultado:")
    output_label.pack(pady=5)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
    output_text.pack(pady=5)

    # Botão para executar o scraper
    def execute_scraper():
        source = url_entry.get().strip()
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            run_scraper(source, output_text)

    scrape_button = tk.Button(root, text="Executar Scraper", command=execute_scraper)
    scrape_button.pack(pady=10)

    # Iniciar loop da interface gráfica
    root.mainloop()

# Função para executar o scraper
def run_scraper(source: str, output_widget: scrolledtext.ScrolledText):
    try:
        # Verificando a conexão de rede
        try:
            response = requests.head(source, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao verificar a conexão de rede:\n{e}")
            return

        # Configuração do scraper com prompt e esquema
        prompt = "Me retorne um scrapping da seguinte página web"
        smart_scraper_graph = SmartScraperGraph (
            prompt=prompt,
            source=source,
            config=GRAPH_CONFIG,
            schema=ResponseSchema,
        )

        # Executando o scraper
        result = smart_scraper_graph.run()

        try:
            # Verifique se result é um dicionário e exiba o conteúdo
            if (result['tag'] != '' and result['tag'] != 'NA'):
                print(f'Result tag = {result['tag']}')
                output_widget.delete(1.0, tk.END)  # Limpar o conteúdo anterior
                output_widget.insert(tk.END, json.dumps(result, indent=4))  # Formatar e exibir
            else:
                print(f'Entrando no else')
                output_widget.delete(1.0, tk.END)  # Limpar o conteúdo anterior
                output_widget.insert(tk.END, HandlerDinamic(url=source, prompt=prompt))  # Formatar e exibir
        except:
            nova_consulta = HandlerDinamic(url=source, prompt=prompt)
            print(f'Entrando no except com url={source} e prompt={prompt}')
            output_widget.delete(1.0, tk.END)  # Limpar o conteúdo anterior
            output_widget.insert(tk.END, HandlerDinamic(url=source, prompt=prompt))  # Formatar e exibir

    except Exception as e:
        messagebox.showerror("Erro no Scraper", f"Erro ao executar o scraper:\n{type(e).__name__} - {str(e)}")
