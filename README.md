# Análise de Dados da COVID-19: Casos vs. Internações em UTI

## 1. Visão Geral

Este projeto realiza uma análise exploratória e inferencial sobre dados da pandemia de COVID-19, com foco na relação entre o número de casos confirmados e as internações em Unidades de Terapia Intensiva (UTI).

A análise se concentra principalmente no Brasil, utilizando dados da Argentina como grupo de comparação para testes de hipótese. O objetivo é responder a perguntas-chave sobre a evolução da pandemia, a pressão sobre o sistema de saúde e as diferenças estatísticas entre países.

As principais análises incluem:
- Estatística descritiva da série temporal de casos e internações.
- Análise de correlação entre novos casos diários e ocupação de UTIs.
- Teste de hipótese para comparar a média de ocupação de UTIs entre Brasil e Argentina.
- Cálculo de probabilidade empírica de eventos críticos (alta ocupação de UTI).

## 2. Fontes de Dados

O projeto utiliza dois conjuntos de dados públicos:

- `total-cases.csv`: Contém o número total acumulado de casos de COVID-19, reportado diariamente para diversos países e para o mundo.
- `covid-hospitalizations.csv`: Contém dados diários de hospitalizações, incluindo a ocupação de leitos de UTI (`Daily ICU occupancy`) por país.

## 3. Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
/
|-- data/
|   |-- covid-hospitalizations.csv
|   |-- total-cases.csv
|
|-- scripts/
|   |-- analise_covid.py
|
|-- README.md
|-- requirements.txt
|
|-- (Saídas Geradas)/
|   |-- series_temporais_brasil.png
|   |-- histograma_uti_brasil.png
|   |-- correlacao_brasil.png
```

## 4. Pré-requisitos

Para executar este projeto, você precisará ter o **Python 3.7+** instalado. As seguintes bibliotecas são necessárias:

- `pandas`
- `matplotlib`
- `seaborn`
- `scipy`

## 5. Instalação

1.  **Clone ou baixe este repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-repositorio>
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```

3.  **Ative o ambiente virtual:**
    - No Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - No macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Instale as dependências a partir do arquivo `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
    *Conteúdo do arquivo `requirements.txt`:*
    ```
    pandas
    matplotlib
    seaborn
    scipy
    ```

## 6. Como Executar a Análise

Com o ambiente configurado e as dependências instaladas, execute o script de análise a partir da pasta raiz do projeto:

```bash
python scripts/analise_covid.py
```

O script irá imprimir os resultados das análises no console e salvar os gráficos gerados na pasta raiz do projeto.

## 7. Detalhes da Análise

O script `analise_covid.py` realiza as seguintes etapas:

### 7.1. Estatística Descritiva
- **Carregamento e Limpeza:** Os dados são carregados, as datas são convertidas e os datasets são filtrados para focar no Brasil e na Argentina.
- **Cálculo de Novos Casos:** O número de novos casos diários para o Brasil é calculado a partir da diferença do total de casos acumulados.
- **Medidas de Tendência Central e Dispersão:** São calculadas a média, mediana, desvio padrão, mínimo e máximo para as variáveis "Novos Casos Diários" e "Ocupação de UTI".
- **Visualização:**
    - Um **gráfico de séries temporais** é gerado para visualizar a evolução de novos casos e da ocupação de UTI no Brasil.
    - Um **histograma** mostra a distribuição de frequência da ocupação diária de UTI.

### 7.2. Análise de Correlação
- **Cálculo:** A **correlação de Pearson** é calculada entre as variáveis "Novos Casos Diários" e "Ocupação de UTI" para quantificar a força da relação linear entre elas.
- **Visualização:** Um **gráfico de dispersão (scatterplot)** é gerado para visualizar essa relação.

### 7.3. Teste de Hipótese (Inferência)
- **Objetivo:** Comparar se a média de ocupação diária de UTI no Brasil é estatisticamente diferente da média na Argentina.
- **Hipóteses:**
    - **H₀ (Nula):** As médias de ocupação de UTI são iguais.
    - **H₁ (Alternativa):** As médias de ocupação de UTI são diferentes.
- **Método:** É utilizado o **Teste t de Welch** (para amostras independentes com variâncias desiguais).
- **Conclusão:** Com base no **p-valor** e em um nível de significância de 5% ($$\alpha = 0.05$$), o script determina se a hipótese nula deve ser rejeitada.

### 7.4. Análise de Probabilidade
- **Objetivo:** Calcular a probabilidade empírica de a ocupação de UTI no Brasil ultrapassar um limiar crítico.
- **Método:**
    1. O **75º percentil** da ocupação de UTI é calculado para definir um limiar de "alta ocupação".
    2. A probabilidade é calculada como a razão entre o número de dias em que a ocupação esteve acima desse limiar e o número total de dias com dados disponíveis.

## 8. Saídas Geradas (Outputs)

Ao executar o script, os seguintes arquivos de imagem são salvos na pasta raiz do projeto:

1.  `series_temporais_brasil.png`: Gráfico de linha mostrando a evolução de novos casos e ocupação de UTI.
2.  `histograma_uti_brasil.png`: Histograma da distribuição da ocupação de UTI no Brasil.
3.  `correlacao_brasil.png`: Gráfico de dispersão mostrando a correlação entre novos casos e ocupação de UTI.