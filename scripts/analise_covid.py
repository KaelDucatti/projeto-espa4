import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

def run_analysis():
    # --- 1. Carregamento e Preparação dos Dados ---
    print("Carregando e preparando os dados...")
    
    # Carregar dados de hospitalizações
    try:
        df_hosp = pd.read_csv('data/covid-hospitalizations.csv')
    except FileNotFoundError:
        print("Erro: Arquivo 'covid-hospitalizations.csv' não encontrado na pasta 'data/'.")
        return

    # Carregar dados de casos totais
    try:
        df_cases = pd.read_csv('data/total-cases.csv')
    except FileNotFoundError:
        print("Erro: Arquivo 'total-cases.csv' não encontrado na pasta 'data/'.")
        return

    # Converter coluna 'date' para datetime
    df_hosp['date'] = pd.to_datetime(df_hosp['date'])
    df_cases['date'] = pd.to_datetime(df_cases['date'])

    # Filtrar dados de UTI para Brasil e Argentina
    df_hosp_br = df_hosp[
        (df_hosp['entity'] == 'Brazil') & 
        (df_hosp['indicator'] == 'Daily ICU occupancy')
    ].copy()
    
    df_hosp_ar = df_hosp[
        (df_hosp['entity'] == 'Argentina') & 
        (df_hosp['indicator'] == 'Daily ICU occupancy')
    ].copy()

    # Preparar dados de casos para o Brasil
    df_cases_br = df_cases[['date', 'Brazil']].copy()
    df_cases_br.rename(columns={'Brazil': 'total_cases'}, inplace=True)
    df_cases_br.sort_values('date', inplace=True)
    df_cases_br['new_cases'] = df_cases_br['total_cases'].diff().fillna(0)
    
    # Juntar os dataframes do Brasil
    df_br_merged = pd.merge(df_cases_br, df_hosp_br, on='date', how='inner')
    df_br_merged.rename(columns={'value': 'icu_occupancy'}, inplace=True)

    print("Dados preparados com sucesso.\n")

    # --- 2. Análise de Estatística Descritiva (Brasil) ---
    print("--- Análise de Estatística Descritiva (Brasil) ---")
    desc_stats = df_br_merged[['new_cases', 'icu_occupancy']].describe()
    print(desc_stats)
    
    # Gráfico de Séries Temporais
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    color = 'tab:blue'
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Novos Casos Diários', color=color)
    ax1.plot(df_br_merged['date'], df_br_merged['new_cases'], color=color, label='Novos Casos Diários')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Ocupação Diária de UTI', color=color)
    ax2.plot(df_br_merged['date'], df_br_merged['icu_occupancy'], color=color, label='Ocupação Diária de UTI')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Evolução de Novos Casos e Ocupação de UTI no Brasil')
    fig.tight_layout()
    plt.savefig('series_temporais_brasil.png')
    plt.show()
    print("\nGráfico 'series_temporais_brasil.png' salvo.")

    # Histograma da Ocupação de UTI
    plt.figure(figsize=(10, 6))
    sns.histplot(df_br_merged['icu_occupancy'].dropna(), kde=True, bins=30)
    plt.title('Distribuição da Ocupação Diária de UTI no Brasil')
    plt.xlabel('Número de Pacientes em UTI')
    plt.ylabel('Frequência')
    plt.savefig('histograma_uti_brasil.png')
    plt.show()
    print("Gráfico 'histograma_uti_brasil.png' salvo.\n")

    # --- 3. Análise de Correlação (Brasil) ---
    print("--- Análise de Correlação (Brasil) ---")
    correlation = df_br_merged['new_cases'].corr(df_br_merged['icu_occupancy'])
    print(f"Correlação de Pearson entre Novos Casos e Ocupação de UTI: {correlation:.4f}")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_br_merged, x='new_cases', y='icu_occupancy', alpha=0.5)
    plt.title('Correlação entre Novos Casos e Ocupação de UTI no Brasil')
    plt.xlabel('Novos Casos Diários')
    plt.ylabel('Ocupação Diária de UTI')
    plt.savefig('correlacao_brasil.png')
    plt.show()
    print("Gráfico 'correlacao_brasil.png' salvo.\n")

    # --- 4. Análise de Inferência (Teste de Hipótese) ---
    print("--- Teste de Hipótese: Brasil vs. Argentina ---")
    
    # Limpar NaNs para o teste t
    icu_br = df_hosp_br['value'].dropna()
    icu_ar = df_hosp_ar['value'].dropna()

    print(f"Média de ocupação de UTI - Brasil: {icu_br.mean():.2f}")
    print(f"Média de ocupação de UTI - Argentina: {icu_ar.mean():.2f}")

    # Realizar o teste t
    t_stat, p_value = ttest_ind(icu_br, icu_ar, equal_var=False) # Welch's t-test
    
    print(f"Estatística t: {t_stat:.4f}")
    print(f"P-valor: {p_value:.4f}")

    alpha = 0.05
    if p_value < alpha:
        print("Conclusão: Rejeitamos a hipótese nula. Há uma diferença significativa entre as médias de ocupação de UTI.")
    else:
        print("Conclusão: Não rejeitamos a hipótese nula. Não há evidência de diferença significativa.")
    print("\n")

    # --- 5. Análise de Probabilidade (Brasil) ---
    print("--- Análise de Probabilidade (Brasil) ---")
    
    percentil_75 = df_br_merged['icu_occupancy'].quantile(0.75)
    print(f"Valor do 75º percentil para ocupação de UTI: {percentil_75:.2f}")
    
    dias_acima_limiar = df_br_merged[df_br_merged['icu_occupancy'] > percentil_75].shape[0]
    total_dias = df_br_merged['icu_occupancy'].notna().sum()
    
    probabilidade = dias_acima_limiar / total_dias
    
    print(f"Probabilidade de a ocupação de UTI exceder {percentil_75:.2f}: {probabilidade:.2%}")

if __name__ == '__main__':
    run_analysis()
