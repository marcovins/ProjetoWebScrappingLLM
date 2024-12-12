import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter.ttk import Progressbar
from threading import Thread
from src.Scrapping.Scrapper import run_static_scraper, run_dynamic_scraper, generate_markdown_content

def start_gui():
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("1000x750")

    tk.Label(root, text="Insira a URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=100)
    url_entry.pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    output_text1 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15)
    output_text1.grid(row=1, column=0, padx=20, pady=5)
    output_text2 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15)
    output_text2.grid(row=1, column=1, padx=20, pady=5)

    progress = Progressbar(root, mode="indeterminate")
    progress.pack(pady=10)

    def thread_done():
        execute_button.config(state=tk.NORMAL)
        progress.stop()

    def execute_scraper(source):
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            execute_button.config(state=tk.DISABLED)
            progress.start()
            output_text1.delete("1.0", tk.END)
            output_text2.delete("1.0", tk.END)
            Thread(target=run_static_scraper, args=(source, thread_done, output_text1)).start()
            Thread(target=run_dynamic_scraper, args=(source, thread_done, output_text2)).start()

    execute_button = tk.Button(root, text="Executar Scraper", command=lambda: execute_scraper(url_entry.get().strip()))
    execute_button.pack(pady=10)
    root.mainloop()