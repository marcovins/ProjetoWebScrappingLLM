import json
import re

def limpar_json(input_json):
    # O input_json é uma string JSON que pode conter texto extra (markdown, por exemplo)
    
    # Tentamos isolar o conteúdo JSON dentro da chave 'result' do input JSON
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


def texto_para_json(texto):
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

