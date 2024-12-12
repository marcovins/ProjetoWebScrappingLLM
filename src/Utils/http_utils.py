from src.Utils.imports import logging, MODEL_URL_REQUEST, PROMPT, schema
import requests

def make_request_to_model(data, promptOpcional: str = None):
    try:
        if promptOpcional:
                prompt = f"{promptOpcional}{data}"
        else:
             prompt = f"{PROMPT}\nEstrutura JSON: {schema}\nDados: {data}"
        requisicao = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(url=MODEL_URL_REQUEST, json=requisicao)
        response.raise_for_status()
        return response.json().get("response", "Erro na resposta do modelo")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição ao modelo: {e}")
        return None
