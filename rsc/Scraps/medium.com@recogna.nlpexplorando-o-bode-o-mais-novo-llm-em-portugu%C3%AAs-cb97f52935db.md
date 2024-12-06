# **Explorando o Bode: O mais novo LLM em Português**

[![Recogna NLP](https://miro.medium.com/v2/da:true/resize:fill:44:44/0*EUXEyHSxqzu-QJjP)](/@recogna.nlp?source=post_page---byline--cb97f52935db--------------------------------)

[Recogna NLP](/@recogna.nlp?source=post_page---byline--cb97f52935db--------------------------------)

·

[Follow](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F44da42865b40&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40recogna.nlp%2Fexplorando-o-bode-o-mais-novo-llm-em-portugu%C3%AAs-cb97f52935db&user=Recogna+NLP&userId=44da42865b40&source=post_page-44da42865b40--byline--cb97f52935db---------------------post_header-----------)

8 min read

·

Jan 30, 2024

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2Fcb97f52935db&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40recogna.nlp%2Fexplorando-o-bode-o-mais-novo-llm-em-portugu%25C3%25AAs-cb97f52935db&user=Recogna+NLP&userId=44da42865b40&source=---header_actions--cb97f52935db---------------------clap_footer-----------)

20

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fcb97f52935db&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40recogna.nlp%2Fexplorando-o-bode-o-mais-novo-llm-em-portugu%25C3%25AAs-cb97f52935db&source=---header_actions--cb97f52935db---------------------bookmark_footer-----------)

Share

![](https://miro.medium.com/v2/resize:fit:323/1*eTPim0DJ6Fp7fQ-PK7qkNQ.png)

S e você já se aventurou pelo vasto universo da inteligência artificial e do processamento de linguagem natural, provavelmente já se deparou com a escassez de modelos robustos e eficazes em língua portuguesa. No entanto, há uma nova esperança no horizonte linguístico: o Bode.

Neste artigo, apresentaremos uma análise detalhada da arquitetura do Bode, acompanhada de uma ilustração prática de sua aplicação em uma tarefa específica: a análise de sentimentos. Para mais informações, convidamos o leitor a visitar a página do na qual está publicado o modelo proposto.

# Introdução

Bode é um modelo de linguagem, do inglês Large Language Model (LLM), projetado especificamente para o português. Seu nascimento ocorreu a partir do fine-tuning do modelo LLaMa 2, utilizando o dataset Alpaca traduzido para o português pelos autores do Cabrita, o Bode foi concebido para suprir as lacunas deixadas por modelos clássicos, como o próprio LLaMa, que, apesar de responderem a prompts em português, muitas vezes cometem erros gramaticais e podem até gerar respostas em inglês.

**Contexto do Desenvolvimento**

A iniciativa de criar o Bode surgiu da necessidade de preencher o vácuo de modelos de linguagem para o idioma português. Enquanto algumas opções estão disponíveis, a maioria delas carece do tamanho e da especificidade necessários para tarefas complexas de processamento de linguagem natural. O Bode, com seus impressionantes 13 bilhões de parâmetros, oferece uma solução mais robusta e especializada.

# Detalhes do Modelo

![](https://miro.medium.com/v2/resize:fit:700/0*47lC9aIBGZuHzbDU)

Fonte: 

# Modelo Base: LLaMa 2

O Bode herda sua base do LLaMa 2, um modelo já estabelecido no cenário de processamento de linguagem natural.

**Dataset de Treinamento: Alpaca**

O treinamento do Bode foi realizado através do fine-tuning no dataset Alpaca traduzido para o português. Esse conjunto de dados, focado em instruções, proporcionou ao modelo uma compreensão profunda da língua portuguesa.

# Idioma: Português

Ao contrário de modelos mais generalistas, em relação ao idioma, o Bode foi concebido exclusivamente para o português, resultando em respostas mais precisas.

# Treinamento e Dados

O processo de treinamento do Bode envolveu o fine-tuning a partir do LLaMa 2, utilizando o dataset Alpaca. Essa abordagem, aliada ao poder computacional do Supercomputador Santos Dumont do LNCC, resultou em um modelo capaz de lidar com tarefas complexas em português.

# Uso Recomendado

Embora o Bode possa ser executado em uma CPU, é altamente recomendável utilizar o Kaggle com GPU para aproveitar todo o potencial do modelo. A biblioteca Transformers do HuggingFace facilita a integração do Bode em seus projetos, mas atenção: é necessário obter autorização de acesso ao LLaMa 2 para utilizá-lo plenamente.

Ao utilizar o Bode, uma das aplicações empolgantes que se destacam é a análise de sentimentos, uma tarefa clássica na área de processamento de linguagem natural. A análise de sentimentos permite determinar a polaridade emocional de um texto, classificando-o como positivo, negativo ou neutro, por exemplo. Essa tarefa é valiosa em uma variedade de cenários, desde avaliações de produtos até monitoramento de redes sociais.

**Análise de Sentimentos: Uma Breve Introdução**

A análise de sentimentos é um problema importante na área de processamento de linguagem natural (PLN), focada em compreender e extrair as emoções expressas em um texto. A capacidade de identificar se uma declaração é positiva, negativa ou neutra é essencial para empresas que desejam entender a percepção pública de seus produtos, serviços ou marcas, por exemplo.

Com o avanço das tecnologias de LLMs, como o Bode, torna-se possível automatizar e aprimorar significativamente a análise de sentimentos, mesmo em cenários com poucos dados disponíveis para treinamento. Esses modelos têm a capacidade de capturar nuances contextuais, entender sarcasmo, e lidar com uma variedade de expressões emocionais, o que os torna instrumentos poderosos para essa tarefa.

Neste artigo avaliamos o desempenho do Bode em realizar a análise de sentimentos em uma base de tweets em português. O experimento foi conduzido seguindo a abordagem Zero Shot, sem realizar o ajuste fino do modelo a esta base específica. A boa performance de LLMs em tarefas para as quais ele sequer foi treinado especificamente é um dos grandes atrativos desses modelos.

**Avaliação da Análise de Sentimentos com LLMs**

A avaliação de desempenho na análise de sentimentos é frequentemente realizada por meio de métricas como precisão, recall, F1-score e matriz de confusão. Essas métricas permitem medir quão bem o modelo classifica corretamente as diferentes polaridades emocionais, fornecendo uma visão clara de sua eficácia.

# Vamos à prática!

Caso queira mais informações sobre o experimento realizado, disponibilizamos todo o código e explicação . Agora, mãos à obra!

Antes de começar, precisamos instalar algumas bibliotecas que serão importantes em nossa implementação.

```
!pip install accelerate==0.25.0 bitsandbytes==0.41.2.post2
```

Com as instalações finalizadas, vamos importar as bibliotecas que utilizaremos nesta implementação.

```
import pandas as pdfrom transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfigimport transformersimport torchfrom getpass import getpass
```

Com as instalações e importações realizadas, agora vamos instanciar nosso modelo, o dataset de análise de sentimentos que iremos utilizar, além de chamar a função getpass, onde colocaremos nossa chave do LLaMa 2.

Obs: Neste exemplo, vamos analisar um dataset muito utilizado de tweets em português disponibilizados na plataforma do Kaggle, para mais informações sobre este dataset,. Para tornar mais rápido nosso experimento, vamos utilizar apenas 200 dados de Teste disponíveis neste dataset.

```
llm_model = ‘recogna-nlp/bode-7b-alpaca-pt-br-no-peft’dataset_path = ‘/kaggle/input/portuguese-tweets-for-sentiment-analysis/TestDatasets/Test.csv’hf_auth = getpass()df = pd.read_csv(dataset_path, delimiter=’;’)pdf = pd.concat([df[:100], df[2500:2600]])
```

Com as instâncias feitas, vamos carregar nosso modelo:

```
print(“Carregando LLM…\n”)model = AutoModelForCausalLM.from_pretrained(llm_model, trust_remote_code=True, return_dict=True, load_in_4bit=True, device_map=’auto’, token=hf_auth)tokenizer = AutoTokenizer.from_pretrained(llm_model, token=hf_auth)model = model.eval()
```

Após carregado o nosso modelo, podemos criar o pipeline de geração de texto:

```
generate_text = transformers.pipeline(model=model,tokenizer=tokenizer,task=’text-generation’,torch_dtype=torch.bfloat16,trust_remote_code=True,)
```

Para a realização deste experimento, vamos utilizar duas abordagens conhecidas: zero-shot e incontext-learning. A primeira abordagem consiste em realizar o experimento sem treinamento prévio específico, ou seja, executar a tarefa pela primeira vez sem nenhum conhecimento anterior direcionado à mesma. Já na segunda abordagem, utilizamos um contexto específico para que o BODE, compreenda e aprenda com base no prompt passado. Dessa forma, o modelo tomará uma decisão com base no conhecimento adquirido durante o treinamento, utilizando o contexto contido no prompt de entrada.

```
prompt = “Você é um assistente de perguntas e respostas. Cada contexto passado será um tweet que está vinculada a um sentimento correspondente. \No total, são 2 tipos de sentimentos: Positivo e Negativo. O seu objetivo é dado um tweet, encontrar qual é o seu sentimento correspondente. \Abaixo estão alguns exemplos:\n Tweet: :D que lindo dia ! Resposta: Positivo\n\Tweet: eu tô tão cansado :( Resposta: Negativo\n\Dado o contexto, responda em qual dos 3 tipos de sentimentos o tweet a seguir se enquadra.\n”
```

Com base na instrução fornecida, procedemos a uma iteração no conjunto de dados predefinido contendo 200 entradas para realizar a classificação dos tweets. A fim de avaliar a precisão da resposta fornecida pelo BODE, aplicamos os mesmos parâmetros utilizados no conjunto de dados, onde atribuímos o valor 1 para tweets positivos e 0 para tweets negativos. É conhecido que os LLMs têm a capacidade de gerar respostas mais extensas do que simplesmente as palavras “Positivo” e “Negativo”. Portanto, implementamos a estratégia de extrair apenas a primeira palavra gerada pelo modelo, uma vez que, em muitas instâncias, essa primeira palavra corresponde à classificação solicitada pelo prompt.

```
preds = []for question in tqdm(df['tweet_text']): input_text = f'Tweet: {question}. Resposta:' res = generate_text(prompt + input_text, do_sample=True, top_k=10, max_length=600, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id ) r = res[0]["generated_text"].split()[-1] if 'Positivo' in r: preds.append(1) elif 'Negativo' in r: preds.append(0) else: print('ERRO:', r) preds.append(2)
```

# **Resultados**

No processo de avaliação do experimento de classificação de sentimentos, empregamos diversas métricas para uma análise abrangente. Essas métricas, provenientes da biblioteca Scikit-learn (Sklearn), incluem a matriz de confusão, precisão, recall, F1 score e acurácia. Vamos sucintamente explicar cada uma delas:

  * Matriz de Confusão:

```
[100 0][ 33 67]
```

A matriz de confusão apresenta a distribuição das predições do modelo em relação aos rótulos reais. No caso, temos 100 instâncias corretamente classificadas como positivas, 67 instâncias corretamente classificadas como negativas, 33 instâncias falsamente classificadas como negativas e nenhuma instância falsamente classificada como positiva.

  * Precisão (Precision):
  * Precision: 0.876



A precisão é a proporção de instâncias positivas previstas corretamente em relação ao total de instâncias previstas como positivas. Neste caso, 87.6% das predições positivas foram corretas.

  * Recall:
  * Recall: 0.835



O recall, também conhecido como sensibilidade ou taxa de verdadeiros positivos, é a proporção de instâncias positivas previstas corretamente em relação ao total de instâncias que são realmente positivas. Aqui, 83.5% das instâncias positivas foram corretamente identificadas.

  * Acurácia (Accuracy):
  * Accuracy: 0.835



A acurácia representa a proporção total de predições corretas em relação ao número total de instâncias. Neste caso, a acurácia geral é de 83.5%.

  * F1 Score:
  * F1 Score: 0.830



O F1 Score é uma métrica que combina precisão e recall em uma única medida. Ele é especialmente útil quando há um desequilíbrio nas classes. Neste contexto, o F1 Score é de 83%, indicando um equilíbrio entre precisão e recall.

Os resultados indicam que o modelo teve um bom desempenho na classificação de sentimentos. A alta precisão sugere que a maioria das predições positivas estava correta, enquanto o recall mostra que o modelo identificou uma grande proporção das instâncias positivas. A acurácia global e o F1 Score, que levam em consideração tanto os verdadeiros positivos quanto os verdadeiros negativos, também estão em um nível satisfatório.

# **Conclusão**

O Bode emerge como uma promissora adição ao panorama de modelos de linguagem em português, apresentando-se como uma solução robusta e especializada para uma diversidade de tarefas em processamento de linguagem natural. Sua capacidade de compreender e gerar texto em português, aliada a um treinamento cuidadoso e a utilização de dados específicos do idioma, contribui para a eficácia e relevância do modelo.

Ao considerarmos a importância de modelos de linguagem em aplicações variadas, o Bode destaca-se como uma ferramenta valiosa para a comunidade que busca avançar em projetos relacionados à compreensão e geração de texto na língua portuguesa. Sua performance em tarefas como classificação de sentimentos, mencionada anteriormente, é um indicativo promissor do potencial abrangente deste modelo.

Além disso, o Bode beneficia-se da contínua contribuição da comunidade, que desempenha um papel crucial na evolução e aprimoramento constante do modelo. A colaboração e o feedback contínuo da comunidade fortalecem sua capacidade de adaptação e refinamento, proporcionando melhorias incrementais ao longo do tempo.

Em suma, o Bode não apenas atende às exigências atuais no campo de processamento de linguagem natural em português, mas também está bem posicionado para desbravar novos horizontes, impulsionando avanços significativos e contribuindo de maneira substancial para o progresso neste domínio em nossa língua materna. Seu impacto promissor evidencia o potencial transformador que modelos de linguagem como o Bode podem ter na forma como interagimos e utilizamos a linguagem no ambiente digital.

# Agradecimentos

O desenvolvimento do Bode foi possível graças ao apoio do Laboratório Nacional de Computação Científica (LNCC/MCTI, Brasil), que forneceu recursos essenciais por meio do supercomputador SDumont. Expressamos nossa gratidão pelo suporte recebido no projeto Fundunesp 2019/00697–8.

Desenvolvido por: e .
