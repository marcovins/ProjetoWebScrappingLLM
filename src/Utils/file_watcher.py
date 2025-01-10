# file_watcher.py

import sys
import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, script, restart_event):
        self.script = script
        self.process = None
        self.last_modified = None
        self.restart_delay = 2  # Tempo de espera para reiniciar (em segundos)
        self.restart_event = restart_event  # Evento para notificar quando reiniciar a GUI

    def start_script(self):
        """Inicia o script e cria um subprocesso."""
        if self.process:
            self.terminate_gui()
        self.process = subprocess.Popen([sys.executable, self.script], stdout=sys.stdout, stderr=sys.stderr)

    def terminate_gui(self):
        """Método para terminar o processo da GUI anterior."""
        if self.process:
            try:
                print("Encerrando o processo anterior...")
                self.process.terminate()  # Encerra o subprocesso
                self.process = None
                print("Processo da GUI encerrado.")
            except Exception as e:
                print(f"Erro ao tentar encerrar o processo: {e}")
        else:
            print("Nenhum processo em execução para terminar.")

    def on_modified(self, event):
        if event.src_path.endswith('gui.py'):
            current_time = time.time()
            if not self.last_modified or (current_time - self.last_modified) > self.restart_delay:
                print(f'Arquivo modificado: {event.src_path}. Reiniciando o script...')
                self.last_modified = current_time
                self.restart_event.set()

def watch_and_restart(script, restart_event):
    """Função para observar as alterações no arquivo e reiniciar o script quando necessário"""
    event_handler = RestartHandler(script, restart_event)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(script), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Mantém o loop funcionando
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
