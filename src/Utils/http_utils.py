from src.Utils.imports import SCRAPS, logging, MODEL_URL_REQUEST, PROMPT, schema, COOKIES, os
from src.Utils.json_utils import limpar_json
import requests

async def make_request_to_model(data, promptOpcional: str = None):
    """
    Envia uma solicitação HTTP POST para um modelo externo, fornecendo os dados de entrada e um prompt opcional 
    para gerar uma resposta do modelo.

    A função monta o prompt para o modelo, incluindo o texto fornecido, e faz uma requisição HTTP POST para o 
    modelo de linguagem, retornando a resposta em formato JSON. Em caso de falha, trata as exceções de rede e 
    outras falhas relacionadas à requisição.

    Args:
        data (str): Dados a serem enviados ao modelo. Pode ser qualquer tipo de entrada que o modelo aceite, 
                    como texto ou dados estruturados.
        promptOpcional (str, opcional): Um prompt adicional para o modelo. Caso não seja fornecido, é utilizado 
                                        o valor de `PROMPT` como padrão.

    Returns:
        dict: A resposta do modelo, retornada em formato JSON. Normalmente, contém o campo 'response' com a 
              resposta gerada pelo modelo.

    Raises:
        Exception: Se houver falhas durante a requisição HTTP, como erros de conexão, timeout, ou falha de 
                   resposta do modelo, uma exceção será levantada.

    Exemplo:
        ```python
        response = await make_request_to_model("Texto de entrada", promptOpcional="Prompt personalizado")
        print(response)
        ```

    Observações:
        - A URL de requisição para o modelo deve estar corretamente configurada em `MODEL_URL_REQUEST`.
        - O modelo utilizado na requisição é especificado no campo `"model"` como `"llama3.2"`.
        - O parâmetro `stream` está definido como `False`, indicando que a resposta não será recebida em fluxo contínuo.
        - O tempo de execução da requisição pode variar dependendo da resposta do modelo, e exceções como `Timeout` e `ConnectionError` são tratadas separadamente para diagnóstico adequado.
    """
    try:
        # Monta o prompt de forma mais concisa e clara
        prompt = f"{promptOpcional if promptOpcional else PROMPT}\ndados: {data}"
        
        requisicao = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }


        # Faz a requisição usando 'with' para garantir que a conexão seja fechada corretamente
        with requests.post(url=MODEL_URL_REQUEST, json=requisicao) as response:
            # Verifica se a resposta foi bem-sucedida
            response.raise_for_status()

            return response.json()['response']

    except requests.exceptions.Timeout as e:
        logging.error(f"Erro de timeout na requisição ao modelo: {e}")
        raise  # Pode levantar novamente ou tratar conforme a necessidade

    except requests.exceptions.ConnectionError as e:
        logging.error(f"Erro de conexão com o modelo: {e}")
        raise

    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro HTTP na requisição ao modelo (status: {response.status_code}): {e}")
        raise

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro geral na requisição ao modelo: {e}")
        raise

    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        raise


def exist_cookies(url: str) -> bool:
    """
    Verifica se existem cookies associados a uma URL específica, verificando se um arquivo de cookies existe.

    A função busca um arquivo JSON contendo cookies para a URL fornecida. O arquivo é salvo em um diretório 
    especificado por `COOKIES` e é nomeado de forma a refletir a URL, com a remoção dos caracteres especiais 
    e a substituição de '://' e '/' por underscores. Se o arquivo de cookies existir, a função retorna 
    o caminho completo para o arquivo, caso contrário, retorna False.

    Args:
        url (str): A URL para a qual os cookies devem ser verificados. A URL deve ser uma string válida, como 
                   'https://example.com'.

    Retorna:
        bool: Retorna o caminho do arquivo de cookies se os cookies existirem para a URL fornecida, 
              caso contrário, retorna False.

    Exemplo:
        ```python
        result = exist_cookies("https://example.com")
        if result:
            print(f"Cookies encontrados: {result}")
        else:
            print("Sem cookies para a URL fornecida.")
        ```

    Observações:
        - O diretório de cookies (`COOKIES`) deve estar corretamente configurado no ambiente.
        - O arquivo de cookies será nomeado com base na URL, portanto, URLs com caracteres especiais, como ':', 
          serão convertidos para um formato compatível com nomes de arquivos.
    """
    path = f"{COOKIES}/{url.replace('://', '_').replace('/', '_')}_cookies.json"
    return (path if os.path.exists(path) else False)

# Função para verificar se o texto contém palavras relacionadas a cookies
def contains_cookie_terms(text):
    """
    Verifica se o texto contém termos relacionados a cookies, como 'cookie', 'aceitar', 'consentimento', entre outros.

    A função analisa a string fornecida para identificar a presença de termos comuns associados a notificações 
    de cookies em sites, como 'aceitar', 'cookies', 'política de privacidade', entre outros. Isso pode ser útil 
    para evitar a coleta de dados de elementos relacionados ao consentimento de cookies durante o scraping.

    Args:
        text (str): Texto a ser analisado. Pode ser um parágrafo ou uma string que contenha informações da página web.

    Retorna:
        bool: Retorna True se o texto contiver algum dos termos relacionados a cookies, e False caso contrário.

    Exemplo:
        ```python
        result = contains_cookie_terms("Este site utiliza cookies para melhorar sua experiência.")
        print(result)  # Saída: True
        ```

    Observações:
        - A verificação é feita de forma insensível a maiúsculas e minúsculas.
        - A função utiliza uma lista de termos predeterminados que são comumente usados em banners ou pop-ups de cookies.
    """
    cookie_terms = ['cookie', 'aceitar', 'consentimento', 'política de privacidade', 'cookies']
    return any(term.lower() in text.lower() for term in cookie_terms)

def validar_resposta(result:str, url:str, metodo:str) -> dict | None:
    if result:
            cleaned_result = result
            if cleaned_result:
                with open(f"{SCRAPS}/json/{url.replace('/', '').replace('https:', '')}.json", "w", encoding="utf-8") as arquivo:
                    arquivo.write(cleaned_result)
                    print("Scraping concluído com sucesso!")
                return {"url": url, "result": cleaned_result, "Método utilizado:": metodo}

    else:
        return None