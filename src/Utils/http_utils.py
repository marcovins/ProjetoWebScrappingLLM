from src.Utils.imports import logging, MODEL_URL_REQUEST, PROMPT, schema, COOKIES, os
from src.Utils.json_utils import limpar_json, texto_para_json
import requests

def make_request_to_model(data, promptOpcional: str = None):
    """
    Envia uma solicitação HTTP POST para um modelo externo com os dados fornecidos.

    Args:
        data (str): Dados a serem enviados na solicitação.
        promptOpcional (str): Solicitação opcional para o modelo.
    Returns:
        dict: Resposta do modelo em formato JSON.

    Raises:
        Exception: Caso a solicitação falhe.
    """
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


def exist_cookies(url: str) -> bool:
    """
    Verifica se existem cookies associados a uma URL específica.

    Args:
        url (str): URL para a qual os cookies devem ser verificados.

    Returns:
        list: Lista de cookies associados à URL ou uma lista vazia se não houver cookies.
    """
    path = f"{COOKIES}/{url.replace('://', '_').replace('/', '_')}_cookies.json"
    return (path if os.path.exists(path) else False)

# Função para verificar se o texto contém palavras relacionadas a cookies
def contains_cookie_terms(text):
    """
    Verifica se o texto contém termos relacionados a cookies.

    Args:
        text (str): Texto a ser analisado.

    Returns:
        bool: True se o texto contiver termos relacionados a cookies, False caso contrário.
    """
    cookie_terms = ['cookie', 'aceitar', 'consentimento', 'política de privacidade', 'cookies']
    return any(term.lower() in text.lower() for term in cookie_terms)

def validar_resposta(result:str, url:str, metodo:str) -> dict | None:
    if result:
            cleaned_result = limpar_json(result)
            if cleaned_result:
                return {"url": url, "result": cleaned_result, "Método utilizado:": metodo}
            
    else:
        return None