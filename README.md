
# Web Scraper Visual

Este é um projeto de **Web Scraper Visual** que utiliza o modelo **SmartScraperGraph** para realizar scraping de páginas web e exibir os resultados de maneira estruturada em uma interface gráfica desenvolvida com **Tkinter**.

A aplicação permite que o usuário insira uma URL e visualize o conteúdo extraído da página web diretamente na interface. O scraper usa um modelo de **LLM (Large Language Model)** para gerar respostas e metadados associados ao conteúdo extraído da página.

**Nota**: Este código necessita de um **modelo LLM** configurado e disponível localmente. No meu caso, estou utilizando uma LLM local, e a configuração está definida por meio de variáveis de ambiente para garantir que o código consiga acessá-la corretamente.

## Funcionalidades

- **Scraping de Página Web**: Extrai o conteúdo de uma página web fornecida pelo usuário.
- **Interface Gráfica**: Desenvolvida com **Tkinter**, a interface permite que o usuário insira URLs e visualize os resultados de scraping de maneira limpa e organizada.
- **Validação de Dados**: Utiliza o **Pydantic** para validar a saída do scraper, garantindo que os dados extraídos estejam estruturados corretamente.
- **Exibição de Metadados**: Além do conteúdo extraído, os metadados como a confiança do modelo e tempo de processamento são exibidos.

## Pré-requisitos

- **Python 3.6+**: Certifique-se de que o Python está instalado em seu ambiente.
- **Bibliotecas necessárias**:
    - `requests`
    - `pydantic`
    - `tkinter` (geralmente já vem instalado com o Python)
    - `scrapegraphai` (biblioteca para scraping com **SmartScraperGraph**)

Você pode instalar as dependências utilizando o `pip`:

```bash
pip install requests pydantic scrapegraphai
```

**Nota**: Para utilizar a aplicação, é necessário configurar uma LLM local. No código, a variável de ambiente `LLM_BASE_URL` é utilizada para apontar para o endpoint da LLM que você deseja usar.

## Como Usar

1. **Iniciar a aplicação**: Ao rodar o script, uma interface gráfica será aberta.
2. **Inserir uma URL**: Digite a URL da página que você deseja realizar o scraping no campo de entrada de texto.
3. **Executar o Scraper**: Clique no botão "Executar Scraper". O conteúdo da página será extraído e exibido na área de resultados.
4. **Resultado**: O scraper irá exibir o conteúdo extraído, juntamente com os metadados, como número de tokens utilizados e tempo de processamento.

### Exemplo de saída de scraping

```json
{
    "descricao": "Texto extraído da página web...",
    "tag": "Categoria da página",
    "tokens_usados": 100,
    "tempo_processamento": 2.3,
    "confianca": 0.95,
    "metadados": {
        "source_url": "http://example.com",
        "author": "Autor do conteúdo"
    }
}
```

## Como Funciona

O código utiliza o modelo **SmartScraperGraph** da biblioteca **scrapegraphai** para realizar o scraping da página web. A resposta gerada pelo scraper é validada usando **Pydantic**, garantindo que os dados extraídos estejam no formato esperado.

Além disso, a interface gráfica foi desenvolvida com **Tkinter** e permite uma experiência simples e intuitiva de uso.

### Arquitetura

- **SmartScraperGraph**: Responsável por realizar o scraping da página web, utilizando o modelo LLM configurado.
- **Pydantic**: Utilizado para validar a saída do scraper e garantir que os dados extraídos estejam no formato correto.
- **Tkinter**: Usado para criar a interface gráfica para interação com o usuário, permitindo uma experiência simples para inserção de URLs e exibição dos resultados.

## Exemplo de código

O código do projeto consiste em um simples scraper, com a seguinte estrutura:

```python
from scrapegraphai.graphs import SmartScraperGraph
import requests
from pydantic import BaseModel, Field
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

# Definição do modelo de validação para a saída do scraper
class ResponseSchema(BaseModel):
    descricao: str
    tag: str
    tokens_usados: int
    tempo_processamento: Optional[float]
    confianca: Optional[float]
    metadados: Optional[dict]

# Função para rodar o scraper
def run_scraper(source: str, output_widget: scrolledtext.ScrolledText):
    try:
        # Verificando a conexão de rede
        try:
            response = requests.head(source, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao verificar a conexão de rede:
{e}")
            return

        # Configuração do scraper com prompt e esquema
        smart_scraper_graph = SmartScraperGraph(
            prompt="Faça um scraping dessa página web",
            source=source,
            config=GRAPH_CONFIG,
            schema=ResponseSchema,
        )

        # Executando o scraper
        result = smart_scraper_graph.run()

        # Exibindo o resultado no widget de saída
        output_widget.delete(1.0, tk.END)  # Limpar o conteúdo anterior
        output_widget.insert(tk.END, result.json(indent=4))

    except Exception as e:
        messagebox.showerror("Erro no Scraper", f"Erro ao executar o scraper:
{type(e).__name__} - {str(e)}")

# Configuração da interface gráfica
def start_gui():
    # Inicialização da janela principal
    root = tk.Tk()
    root.title("Web Scraper Visual")
    root.geometry("600x400")

    # Label e campo de entrada para URL
    url_label = tk.Label(root, text="Insira a URL:")
    url_label.pack(pady=5)

    url_entry = tk.Entry(root, width=80)
    url_entry.pack(pady=5)

    # Texto para saída
    output_label = tk.Label(root, text="Resultado:")
    output_label.pack(pady=5)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
    output_text.pack(pady=5)

    # Botão para executar o scraper
    def execute_scraper():
        source = url_entry.get().strip()
        if not source:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma URL válida.")
        else:
            run_scraper(source, output_text)

    scrape_button = tk.Button(root, text="Executar Scraper", command=execute_scraper)
    scrape_button.pack(pady=10)

    # Iniciar loop da interface gráfica
    root.mainloop()

# Ponto de entrada
if __name__ == "__main__":
    start_gui()
```

## Contribuindo

Se você deseja contribuir para este projeto, siga os passos abaixo:

1. **Faça um fork do repositório**.
2. **Crie uma branch** para suas modificações (`git checkout -b feature-name`).
3. **Faça commit das suas alterações** (`git commit -am 'Adiciona nova funcionalidade'`).
4. **Envie a branch para o repositório remoto** (`git push origin feature-name`).
5. **Abra um Pull Request** para que suas alterações possam ser revisadas e mescladas ao projeto principal.

## Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se você tiver dúvidas ou sugestões, não hesite em abrir uma **issue** ou enviar um **pull request**. Fique à vontade para entrar em contato!

---

Obrigado por usar o **Web Scraper Visual**!