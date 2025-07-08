### Obs.: a proposta de projeto completa se encontra na raiz do repositório, no arquivo [Projeto_2025s1.pdf](Projeto_2025s1.pdf)

# Análise de Dados da COVID-19: Casos vs. Internações em UTI

## 1. Visão Geral

Este projeto realiza uma análise exploratória e inferencial sobre dados da pandemia de COVID-19, com foco na relação entre o número de casos confirmados e as internações em Unidades de Terapia Intensiva (UTI).

Este trabalho foi desenvolvido para atender aos requisitos de uma disciplina de análise de dados, aplicando conceitos teóricos em um estudo de caso prático. A análise se concentra na **França (`France`)**, utilizando dados da **Alemanha (`Germany`)** como grupo de comparação.

## 2. Objetivos e Perguntas de Análise

Seguindo a metodologia de "fazer perguntas à base de dados", o projeto busca responder às seguintes questões:

1.  **(Estatística Descritiva)** Como evoluíram o número de novos casos e as internações em UTI na França durante o período observado?
2.  **(Estatística Descritiva)** Qual a distribuição estatística e a correlação entre o aumento de novos casos diários e o aumento de internações em UTI?
3.  **(Inferência)** A média de ocupação diária de UTIs na França foi significativamente diferente da média na Alemanha?
4.  **(Probabilidade)** Qual a probabilidade de a ocupação de UTIs na França ultrapassar um limiar crítico em um dia qualquer?

## 3. Fontes de Dados

O projeto utiliza dois conjuntos de dados públicos do Our World in Data:

- `total_cases.csv`: Contém o número total acumulado de casos de COVID-19.
- `covid-hospitalizations.csv`: Contém dados diários de hospitalizações.

## 4. Estrutura do Projeto

```
/
|-- data/
|-- scripts/
|   |-- analise_covid.py
|
|-- resultados/
|   |-- series_temporais.png
|   |-- histograma_uti.png
|   |-- correlacao.png
|
|-- main.py
|-- README.md
|-- ... (outros arquivos de ambiente)
```

## 5. Pré-requisitos e Instalação

Para executar este projeto, você precisará do **Python 3.7+** e das bibliotecas `pandas`, `matplotlib`, `seaborn`, `scipy`.

1.  **Crie e ative um ambiente virtual.**
2.  **Instale as dependências:**
    ```bash
    pip install pandas matplotlib seaborn scipy
    ```

## 6. Como Executar a Análise

Com o ambiente configurado, execute o script a partir da pasta raiz do projeto:

```bash
python main.py
```

O script irá imprimir os resultados numéricos no console e salvar os gráficos gerados na pasta `resultados/`. A interpretação detalhada desses resultados está descrita abaixo.

## 7. Detalhes da Análise e Cálculos Realizados

O script `scripts/analise_covid.py` realiza as seguintes análises, conforme os conteúdos da disciplina:

### a. Estatística Descritiva
- **Preparação dos Dados:** Os dados são carregados e o arquivo de casos é transformado do formato "largo" para "longo" (`pandas.melt`) para permitir uma junção robusta com os dados de hospitalizações.
- **Cálculo de Novos Casos:** O número de novos casos diários é calculado usando `groupby('entity').diff()`.
- **Análise de Correlação:** A **Correlação de Pearson** é calculada para medir a força da relação linear entre novos casos e ocupação de UTI.

### b. Inferência (Teste de Hipótese)
- **Método:** É utilizado o **Teste t de Welch** para comparar as médias de ocupação de UTI entre a França e a Alemanha.
- **Conclusão:** O **p-valor** é comparado com um nível de significância de 5% para determinar se a diferença entre as médias é estatisticamente significativa.

### c. Probabilidade
- **Método:** A probabilidade empírica de a ocupação de UTI ultrapassar o **75º percentil** é calculada para quantificar a frequência de períodos de alta pressão hospitalar.

## 8. Resultados e Interpretação

A execução do script gerou os seguintes resultados, que são interpretados abaixo.

### a. Estatística Descritiva (Análise da França)

- **Resultados Numéricos:**
  - `count`: 1.109 dias de dados
  - `mean new_cases`: ~35.000
  - `std new_cases`: ~171.500
  - `mean icu_occupancy`: ~2.047
  - `min/max icu_occupancy`: 344 / 7.019

- **Interpretação:**
  A análise descritiva para a França, baseada em 1.109 dias de dados, revela a natureza volátil da pandemia. A média de novos casos diários foi de aproximadamente 35.000, mas com um desvio padrão extremamente elevado, indicando a ocorrência de ondas pandêmicas com picos de infecção muito acima da média. O sistema de saúde enfrentou uma pressão similarmente variável, com a ocupação de UTIs por pacientes de COVID-19 variando de um mínimo de 344 para um pico alarmante de mais de 7.000, com uma média diária de 2.047 leitos ocupados. Esses números demonstram os desafios significativos enfrentados pelo sistema hospitalar francês.

### b. Análise de Correlação (França)

- **Resultado Numérico:**
  - `Correlação de Pearson`: 0.0587

- **Interpretação:**
  A análise de correlação de Pearson entre o número de *novos casos diários* e a *ocupação diária de UTI* no mesmo dia resultou em um coeficiente de 0.0587. Este valor, muito próximo de zero, indica que **não há uma correlação linear forte e imediata** entre as duas variáveis. Este resultado, embora contraintuitivo, é esperado e pode ser explicado por fatores como o **lag temporal** (atraso entre o diagnóstico e a necessidade de UTI), o **impacto da vacinação** e a **menor severidade de novas variantes**, que fizeram com que um grande número de casos não se traduzisse em um aumento proporcional de internações graves.

### c. Inferência (Teste de Hipótese: França vs. Alemanha)

- **Resultados Numéricos:**
  - `Média de ocupação de UTI (França)`: 2046.52
  - `Média de ocupação de UTI (Alemanha)`: 1771.24
  - `P-valor`: 0.0000

- **Interpretação:**
  Para comparar a carga sobre os sistemas de saúde, foi realizado um teste t entre a média de ocupação diária de UTI na França (2046.52) e na Alemanha (1771.24). O resultado produziu um **p-valor extremamente baixo (p < 0.0001)**. Como este valor é significativamente menor que o nosso nível de significância (α = 0.05), **rejeitamos a hipótese nula**. Isso nos permite concluir, com alta confiança estatística, que a diferença observada entre as médias não é fruto do acaso. Durante o período analisado, a França teve, em média, uma carga de ocupação de UTIs por COVID-19 **estatisticamente maior** do que a Alemanha.

### d. Probabilidade (Análise da França)

- **Resultado Numérico:**
  - `Probabilidade de a ocupação de UTI exceder 2933.00`: 24.98%

- **Interpretação:**
  A análise de probabilidade empírica foi usada para quantificar a frequência de períodos de alta pressão sobre o sistema de saúde. Definimos um limiar crítico como o 75º percentil da ocupação de UTI (2.933 leitos). O cálculo revelou que a probabilidade de a ocupação de UTI exceder este valor em um dia qualquer foi de **24.98%**. Em termos práticos, isso significa que durante aproximadamente **um em cada quatro dias** do período analisado, o sistema de saúde francês esteve sob uma carga considerada 'alta', com quase 3.000 ou mais pacientes de COVID-19 em tratamento intensivo.