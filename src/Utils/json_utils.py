import json
import re

def limpar_json(input_json):
    """
    Limpa e extrai dados de um JSON embutido dentro de um texto, removendo caracteres indesejados e 
    garantindo a formatação correta do conteúdo JSON.

    A função busca um bloco JSON dentro de uma string de entrada, que pode estar contido entre as marcações 
    de blocos de código (```json e ```) ou simples marcações de código (``` e ```). Ela remove caracteres de 
    controle indesejados (como quebras de linha ou tabulação), extrai o JSON e a URL associada (se presente), 
    e retorna um dicionário limpo.

    Args:
        input_json (str): Texto de entrada que pode conter um JSON embutido, com ou sem a marcação `json`.

    Returns:
        dict: Dicionário contendo a URL extraída (se presente) e o JSON limpo em um campo 'result'.
              Retorna um dicionário vazio em caso de erro ou se a formatação do JSON não for encontrada.

    Raises:
        ValueError: Caso o JSON não seja encontrado corretamente dentro do texto.
        json.JSONDecodeError: Caso o conteúdo JSON embutido não seja válido.

    Exemplo:
        input_text = 'Texto inicial ```json\n{"key": "value"}\n``` Texto final'
        result = limpar_json(input_text)
        print(result)
        # Saída esperada: {'url': 'url_extraída', 'result': {'key': 'value'}}
    """

    try:
        
        # Verifica se a marcação está presente
        if "```json" in input_json and "```" in input_json:

            # Localiza a parte que contém o JSON embutido, após a primeira ocorrência de ```json
            json_start = input_json.find("```json\n")
            json_end = input_json.find("\n```", json_start)

            if json_start == -1 or json_end == -1:
                raise ValueError("Conteúdo JSON não encontrado corretamente no input.")

            # Extrai o JSON em forma de string e limpa as quebras de linha desnecessárias
            result_json = input_json[json_start + len("```json\n"):json_end].strip()

            # Remove caracteres de controle indesejados (como quebras de linha ou tabulação)
            result_json = re.sub(r'[\x00-\x1f\x7f]', '', result_json)  # Remove caracteres de controle ASCII

            # Converte o JSON embutido em um dicionário Python
            result_data = json.loads(result_json)

            # Agora, cria o dicionário de saída com a URL e o JSON limpo
            cleaned_data = {}
            # Tente extrair a URL de forma segura
            url_start = input_json.find('"url":')
            if url_start != -1:
                url_end = input_json.find('"', url_start + len('"url":'))
                if url_end != -1:
                    cleaned_data['url'] = input_json[url_start + len('"url":'):url_end].strip().strip('"')
            
            cleaned_data['result'] = result_data

            return cleaned_data
        
        # Verifica se a marcação está presente
        elif "```" in input_json and "```" in input_json:
            
            # Localiza a parte que contém o JSON embutido, após a primeira ocorrência de ```json
            json_start = input_json.find("```\n")
            json_end = input_json.find("\n```", json_start)

            if json_start == -1 or json_end == -1:
                raise ValueError("Conteúdo JSON não encontrado corretamente no input.")

            # Extrai o JSON em forma de string e limpa as quebras de linha desnecessárias
            result_json = input_json[json_start + len("```\n"):json_end].strip()

            # Remove caracteres de controle indesejados (como quebras de linha ou tabulação)
            result_json = re.sub(r'[\x00-\x1f\x7f]', '', result_json)  # Remove caracteres de controle ASCII

            # Converte o JSON embutido em um dicionário Python
            result_data = json.loads(result_json)

            # Agora, cria o dicionário de saída com a URL e o JSON limpo
            cleaned_data = {}
            # Tente extrair a URL de forma segura
            url_start = input_json.find('"url":')
            if url_start != -1:
                url_end = input_json.find('"', url_start + len('"url":'))
                if url_end != -1:
                    cleaned_data['url'] = input_json[url_start + len('"url":'):url_end].strip().strip('"')
            
            cleaned_data['result'] = result_data

            return cleaned_data
        
    except Exception as e:
        print(f"Erro ao processar o JSON: {e}")
        return {}


def texto_para_json(texto:str) ->dict :
    """
    Converte um texto estruturado em formato de lista com asteriscos (`*`) em um dicionário JSON.

    Esta função é útil quando a função `limpar_json()` retorna um resultado vazio e a resposta da LLM (Language Model) 
    não está no formato esperado. Ela converte um texto onde cada linha que começa com um asterisco (`*`) 
    é interpretada como um par chave-valor no formato 'chave: valor'. As linhas que não seguem esse formato 
    são ignoradas.

    Args:
        texto (str): Texto que será processado para gerar um dicionário. O texto deve ter linhas que começam com 
                     asteriscos (`*`) para indicar pares chave-valor, no formato 'chave: valor'.

    Returns:
        dict: Dicionário gerado a partir do texto. Se ocorrer algum erro durante o processamento, 
              um dicionário com uma chave "error" será retornado, contendo a descrição do erro.

    Exemplo:
        texto = "
        * Nome: João
        * Idade: 30
        * Cidade: São Paulo
        "
        resultado = texto_para_json(texto)
        print(resultado)
        # Saída esperada: {'Nome': 'João', 'Idade': '30', 'Cidade': 'São Paulo'}

    Raises:
        ValueError: Caso o texto não contenha nenhum asterisco (`*`) ou se houver algum erro ao processar o texto.
    """
    try:
        # Localiza o primeiro asterisco e corta a string
        pos = texto.find("*")
        if pos == -1:
            raise ValueError("Nenhum asterisco encontrado no texto.")

        texto_cortado = texto[pos:]  # Corta a string a partir do primeiro asterisco
        
        # Remove os asteriscos e prepara para chave: valor
        linhas = texto_cortado.splitlines()
        resultado = {}
        
        for linha in linhas:
            linha = linha.strip()
            if not linha or not linha.startswith("*"):  # Ignora linhas vazias ou sem asteriscos no início
                continue
            
            linha_sem_asteriscos = linha.replace("*", "").strip()
            if ":" in linha_sem_asteriscos:
                chave, valor = map(str.strip, linha_sem_asteriscos.split(":", 1))  # Divide na primeira ocorrência de ':'
                resultado[chave] = valor
        
        # Retorna o JSON resultante
        return resultado

    except Exception as e:
        return {"error": f"Erro ao processar o texto: {str(e)}"}


