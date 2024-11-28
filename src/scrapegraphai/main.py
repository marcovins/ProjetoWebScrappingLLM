from scrapegraphai.graphs import SmartScraperGraph
import requests
from typing import Optional
from pydantic import BaseModel, Field
import tkinter as tk
from tkinter import messagebox, scrolledtext
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Modelo de validação para a saída do scraper
class ResponseSchema(BaseModel):
    descricao: str = Field(..., description="O texto gerado pela LLM")
    tag: str = Field(..., description="Categoria do site")
    tokens_usados: int = Field(..., ge=0, description="Número de tokens utilizados na geração")
    tempo_processamento: Optional[float] = Field(
        None, ge=0.0, description="Tempo em segundos que levou para gerar a resposta"
    )
    confianca: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Pontuação de confiança do modelo, entre 0 e 1"
    )
    metadados: Optional[dict] = Field(
        None, description="Metadados adicionais retornados pelo modelo"
    )

# Configuração do modelo LLM
MODEL_URL = os.getenv("MODEL_URL")  # Aqui usamos os.getenv para pegar o valor da variável de ambiente

GRAPH_CONFIG = {
    "llm": {
        "model": "llama3.2",
        "temperature": 0,
        "format": "json",
        "base_url": MODEL_URL,  # Agora usamos a variável corretamente
    },
    "embeddings": {
        "model": "nomic-embed-text",
        "base_url": MODEL_URL,  # E aqui também
    },
    "headless": True,
    "verbose": False,
}

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
        smart_scraper_graph = SmartScraperGraph(
            prompt="Faça um scraping dessa página web",
            source=source,
            config=GRAPH_CONFIG,
            schema=ResponseSchema,
        )

        # Executando o scraper
        result = smart_scraper_graph.run()

        # Exibindo o resultado no widget de saída
        output_widget.delete(1.0, tk.END)  # Limpar o conteúdo anterior
        output_widget.insert(tk.END, result.json(indent=4))

    except Exception as e:
        messagebox.showerror("Erro no Scraper", f"Erro ao executar o scraper:\n{type(e).__name__} - {str(e)}")

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

# Ponto de entrada
if __name__ == "__main__":
    start_gui()
