import tkinter as tk
from tkinter import messagebox, scrolledtext
from src.Scrapping.Scrapper import run_static_scraper, run_dynamic_scraper, generate_markdown_content
from threading import Thread

# Interface gráfica
def start_gui():
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("1000x700")  # Ajuste para acomodar todos os widgets

    # Entrada de URL
    tk.Label(root, text="Insira a URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=100)
    url_entry.pack(pady=5)

    # Frame principal para os campos de texto
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Campo para resultado do scraping estático
    tk.Label(frame, text="Resultado Busca Estática (Scrapegraphai):").grid(row=0, column=0, padx=20, pady=5)
    output_text1 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15)
    output_text1.grid(row=1, column=0, padx=20, pady=5)

    # Campo para resultado do scraping dinâmico
    tk.Label(frame, text="Resultado Busca Dinâmica (Selenium, BeautifulSoup):").grid(row=0, column=1, padx=20, pady=5)
    output_text2 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15)
    output_text2.grid(row=1, column=1, padx=20, pady=5)

    # Botão para executar os scrapers (logo abaixo dos campos de scraper)
    execute_button = tk.Button(frame, text="Executar Scraper", command=lambda: execute_scraper(url_entry.get().strip()))
    execute_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Campo para o markdown do conteúdo
    tk.Label(frame, text="Markdown do Conteúdo:").grid(row=3, column=0, columnspan=2, padx=20, pady=5)
    output_text3 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=10)
    output_text3.grid(row=4, column=0, columnspan=2, padx=20, pady=5)

    # Botão para gerar o Markdown (logo abaixo do campo de markdown)
    markdown_button = tk.Button(root, text="Gerar Markdown", command=lambda: generate_markdown(url_entry.get().strip()))
    markdown_button.pack(pady=10)

    # Variável para contar threads concluídas
    threads_completed = [0]

    # Callback para threads
    def thread_done():
        threads_completed[0] += 1
        if threads_completed[0] == 2:  # Ambas as threads concluíram
            execute_button.config(state=tk.NORMAL)

    # Função para executar os scrapers
    def execute_scraper(source):
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            threads_completed[0] = 0  # Resetar contador de threads
            execute_button.config(state=tk.DISABLED)  # Desativar botão durante execução
            output_text1.delete("1.0", tk.END)  # Limpar o texto do resultado anterior
            output_text2.delete("1.0", tk.END)  # Limpar o texto do resultado anterior

            # Iniciar threads para scraping
            Thread(target=run_static_scraper, args=(source, thread_done, output_text1)).start()
            Thread(target=run_dynamic_scraper, args=(source, thread_done, output_text2)).start()

    # Função para gerar o markdown
    def generate_markdown(source):
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida antes de gerar o Markdown.")
        else:
            output_text3.delete("1.0", tk.END)  # Limpar o texto do resultado anterior
            generate_markdown_content(source, output_text3)

    # Iniciar a interface gráfica
    root.mainloop()