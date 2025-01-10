import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import asyncio
from src.Scrapping.Scrapper import run_dynamic_scraper, generate_markdown_content
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

def init_gui(root: tk.Tk):
    """Função para inicializar a interface gráfica."""
    # Criação da interface    
    root.title("Web Scraper Visual")
    root.geometry("1000x750")
    root.resizable(False, False)
    root.wm_attributes("-topmost", True)
    root.grab_set()

    # Configuração do ícone
    icon_path = os.path.join(os.path.dirname(__file__),"rsc", "IUicons", "skull.ico").replace("\\src\\Utils", "")
    root.iconbitmap(icon_path)

    bg_image_path =  os.path.join(os.path.dirname(__file__),"rsc", "IUicons", "bg.jpg").replace("\\src\\Utils", "")
    # Carregando e redimensionando a imagem de fundo
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((1000, 750), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Criando um Label para exibir a imagem de fundo
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Faz a imagem ocupar toda a janela
    
    # Garantindo que a referência à imagem de fundo seja mantida
    bg_label.image = bg_photo  # Isso impede que a imagem seja descartada ao fechar e reiniciar

    # Campo para inserir a URL
    tk.Label(root, text="Insira a URL:", bg="black", fg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10)
    url_entry = tk.Entry(root, width=80, fg="black", font=("Arial", 12))
    url_entry.grid(row=1, column=0, pady=5, padx=125, columnspan=2)

    # Frame para os resultados
    frame = tk.Frame(root)
    frame.grid(row=2, column=0, pady=10)

    # Áreas de texto para mostrar os resultados
    output_text1 = tk.Text(root, wrap=tk.WORD, width=55, height=15)
    output_text1.grid(row=3, column=0, padx=10)
    output_text2 = tk.Text(root, wrap=tk.WORD, width=55, height=15)
    output_text2.grid(row=3, column=1, padx=10)

    # Adicionando texto descritivo ao primeiro ScrolledText
    output_text1.insert(tk.END, "Resultado do Scraping:\n")
    output_text1.insert(tk.END, "Aqui aparecerá o conteúdo coletado do site após a execução do scraper.\n")

    # Adicionando texto descritivo ao segundo ScrolledText
    output_text2.insert(tk.END, "Resultado do Markdown:\n")
    output_text2.insert(tk.END, "Aqui aparecerá o conteúdo gerado a partir da conversão para Markdown.\n")

    # Barra de progresso
    progress = Progressbar(root, mode="indeterminate")
    progress.grid(row=5, column=0, pady=10, padx=100)

    create_buttons(root, output_text1, output_text2, url_entry, progress)

    def on_closing():
        """Função para fechar a janela corretamente"""
        print("Fechando a interface gráfica...")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)


def execute_scraper(source: str, output_text1: tk.Text, progress, execute_button):
    """Executa o scraper em uma nova thread"""
    if not source:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        return
    output_text1.delete("1.0", tk.END)
    progress.start()
    execute_button.config(state=tk.DISABLED)

    def run_scraping():
        asyncio.run(run_scrape_async(url=source, output_widget1=output_text1, progress=progress, execute_button=execute_button))

    Thread(target=run_scraping).start()

def execute_markdown(source: str, output_text2: tk.Text, progress, markdown_button):
    """Executa o markdown em uma nova thread"""
    if not source:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        return
    output_text2.delete("1.0", tk.END)
    markdown_button.config(state=tk.DISABLED)
    progress.start()

    def run_markdown():
        asyncio.run(run_markdown_async(source, output_widget2=output_text2, progress=progress, markdown_button=markdown_button))

    Thread(target=run_markdown).start()

async def run_scrape_async(url: str, output_widget1: tk.Text, progress, execute_button):
    """Função assíncrona para scraper"""
    await run_dynamic_scraper(url, output_widget1)
    on_scraper_complete(progress, execute_button)

def on_scraper_complete(progress, execute_button):
    """Finaliza o scraping"""
    progress.stop()
    execute_button.config(state=tk.NORMAL)

async def run_markdown_async(source: str, output_widget2: tk.Text, progress, markdown_button):
    """Função assíncrona para gerar o conteúdo Markdown"""
    await generate_markdown_content(url=source, output_widget2=output_widget2)
    on_markdown_complete(progress, markdown_button)

def on_markdown_complete(progress, markdown_button):
    """Finaliza a execução do markdown"""
    progress.stop()
    markdown_button.config(state=tk.NORMAL)

def create_buttons(root, output_text1, output_text2, url_entry, progress):
    """Cria os botões e os associa às funções de scraping e markdown"""
    execute_button = tk.Button(root, text="Executar Scraper", command=lambda: execute_scraper(url_entry.get().strip(), output_text1, progress, execute_button), bg="black", fg="white", font=("Arial", 12), relief="raised", bd=0)
    execute_button.grid(row=8, column=0, padx=100, sticky="w")

    markdown_button = tk.Button(root, text="Gerar Markdown", command=lambda: execute_markdown(url_entry.get().strip(), output_text2, progress, markdown_button), bg="black", fg="white", font=("Arial", 12), relief="raised", bd=0)
    markdown_button.grid(row=8, column=0, padx=100, sticky="e")

    # Botões para copiar o conteúdo para a área de transferência
    copy_button1 = tk.Button(root, text="Copiar Resultado do Scraping", command=lambda: copy_to_clipboard(root, output_text1), bg="black", fg="white", font=("Arial", 12), relief="raised", bd=0)
    copy_button1.grid(row=4, column=0, padx=100, sticky="w")

    copy_button2 = tk.Button(root, text="Copiar Resultado do Markdown", command=lambda: copy_to_clipboard(root, output_text2), bg="black", fg="white", font=("Arial", 12), relief="raised", bd=0)
    copy_button2.grid(row=4, column=0, padx=100, sticky="e")

def copy_to_clipboard(root, output_widget):
    """Função para copiar conteúdo para a área de transferência"""
    root.clipboard_clear()
    root.clipboard_append(output_widget.get("1.0", tk.END))
    root.update()
