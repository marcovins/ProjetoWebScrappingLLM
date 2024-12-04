
# Projeto de WebScraping com LLM's 🌐🤖

O seguinte projeto é uma aplicação para extração e exibição de informações de páginas web, utilizando o modelo **SmartScraperGraph** e uma interface gráfica desenvolvida com **Tkinter**. A aplicação combina scraping dinâmico com modelos LLM (Large Language Model) para gerar respostas estruturadas e metadados de páginas web.

> **Nota:** Este projeto exige uma configuração local de modelo LLM e as variáveis de ambiente configuradas corretamente para acessar o modelo.

---

## Funcionalidades 🛠️

- **Scraping Dinâmico e Estático:** 🌍
  - Lida com páginas dinâmicas e estáticas, usando Selenium quando necessário.
- **Interface Gráfica Intuitiva:** 🖥️
  - Desenvolvida com **Tkinter**, facilita a interação para inserir URLs e exibir resultados.
- **Fallback Dinâmico:** 🔄
  - Usa `HandlerDinamic` para páginas com conteúdo carregado dinamicamente.
- **Validação Estruturada:** ✅
  - Implementa **Pydantic** para validar e organizar os dados extraídos.
- **Resultados Detalhados:** 📊
  - Exibe dados extraídos, como descrições, tags, confiança do modelo e tempo de processamento.

---

## Requisitos ⚙️

### Dependências de Sistema 💻

- **Python 3.6+** 
- **Google Chrome** e **ChromeDriver** (para scraping dinâmico com Selenium).

### Dependências de Python 📦

- `requests`
- `pydantic`
- `tkinter` (disponível por padrão em distribuições do Python)
- `selenium`
- `scrapegraphai`
- `beautifulsoup4`
- `python-dotenv`
  
Instale todas as dependências com:

```bash
pip install -r requirements.txt
```

> **Nota:** Configure uma LLM local. As variáveis de ambiente `MODEL_URL` e `PROMPT` devem apontar para o endpoint configurado.

---

## Como Usar 📝

1. **Configurar as variáveis de ambiente:** ⚙️
   - Crie um arquivo `.env` e configure:
     ```env
     MODEL_URL=http://localhost:5000
     PROMPT="Extraia informações estruturadas desta página"
     ```

2. **Iniciar a aplicação:** 🚀
   - Execute o script principal:
     ```bash
     python src/main.py
     ```

3. **Interagir com a interface:** 🎮
   - Insira a URL no campo de texto.
   - Clique em "Executar Scraper".
   - Visualize os resultados detalhados na área de saída.

---

## Exemplo de Saída 💡

Um exemplo de resposta estruturada:

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

---

## Estrutura do Projeto 🗂️

```plaintext
rsc/
├──chromedriver-win32/ # Arquivos necessários para utilizar o chromedriver
│   └──chromedriver.exe 
│   └──LICENSE,chromedriver
│   └──THIRD_PARTY_NOTICES.chromedriver

src/
├──Scrapping
│   └── Scrapper.py           # Script principal com interface gráfica
│   └── DinamicScrapper.py    # Scraper dinâmico com Selenium
│   └──main.py # Arquivo principal de execução
├── Schemas/
│   └── ResponseSchema.py # Esquema de validação dos dados extraídos
test/
├── Scrapper_tests.py # Arquivo de testes
```

---

## Contribuindo 🤝

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para suas alterações (`git checkout -b feature/descricao`).
3. Faça commit das mudanças (`git commit -m "Descrição das mudanças"`).
4. Envie a branch para o repositório remoto (`git push origin feature/descricao`).
5. Abra um Pull Request.

---

## Contato 📬

Se você tiver dúvidas, sugestões ou encontrar problemas, abra uma **issue** ou envie um **pull request**.
