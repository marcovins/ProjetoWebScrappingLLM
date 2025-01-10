from threading import Thread, Event
import tkinter as tk
import os
from src.Utils.file_watcher import watch_and_restart
from src.Utils.gui import init_gui

def run_tkinter(restart_event):
    """Função principal para rodar a interface gráfica"""

    # Loop para monitorar o evento de reinicialização
    while True:
        current_root = tk.Tk()
        init_gui(current_root)
        print(current_root.mainloop())

        if restart_event.is_set():
            current_root.destroy() 
            restart_event.clear()
            print("Fechando a interface gráfica...")
            print("Reiniciando a GUI...")
        else:
            break

if __name__ == "__main__":
    # Caminho para o script a ser monitorado
    script_to_run = os.path.join(os.path.dirname(__file__), "Utils", "gui.py").replace("\\Scrapping", "")
    
    # Evento de reinicialização
    restart_event = Event()

    # Inicia a thread de monitoramento
    watch_thread = Thread(target=watch_and_restart, args=(script_to_run, restart_event))
    watch_thread.daemon = True  # Faz a thread ser finalizada quando o programa terminar
    watch_thread.start()

    # Executa a interface gráfica
    run_tkinter(restart_event)  # Inicia a interface com a reinicialização quando necessário
