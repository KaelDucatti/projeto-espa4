import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import os

def run_analysis():
    """
    Executa a análise completa dos dados de COVID-19, utilizando uma abordagem robusta
    de transformação de dados (melt) para garantir a junção correta dos arquivos.
    """
    DATA_DIR = 'data'
    OUTPUT_DIR = 'resultados'
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Carregando os dados...")
    
    hosp_path = os.path.join(DATA_DIR, 'covid-hospitalizations.csv')
    cases_path = os.path.join(DATA_DIR, 'total-cases.csv')

    try:
        df_hosp = pd.read_csv(hosp_path)
        df_cases_wide = pd.read_csv(cases_path)
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado. Verifique o caminho: {e.filename}")
        return

    print("Transformando e preparando os dados...")
    
    # --- ETAPA 1: Transformar o arquivo de casos de 'wide' para 'long' ---
    df_cases_long = pd.melt(
        df_cases_wide, 
        id_vars=['date'], 
        var_name='entity', 
        value_name='total_cases'
    )
    
    # Converter datas para o formato datetime
    df_cases_long['date'] = pd.to_datetime(df_cases_long['date'])
    df_hosp['date'] = pd.to_datetime(df_hosp['date'])
    
    # Limpar nomes de entidades
    df_cases_long['entity'] = df_cases_long['entity'].str.strip()
    df_hosp['entity'] = df_hosp['entity'].str.strip()

    # --- ETAPA 2: Unir os dois DataFrames 'long' em um só ---
    df_merged = pd.merge(
        df_cases_long, 
        df_hosp, 
        on=['date', 'entity'], 
        how='inner' # 'inner' garante que só teremos dados onde há casos E hospitalizações
    )

    # --- ETAPA 3: Filtrar para o indicador de interesse ---
    INDICADOR_UTI = 'Daily ICU occupancy'
    df_analysis_ready = df_merged[df_merged['indicator'] == INDICADOR_UTI].copy()
    
    # Calcular novos casos diários (APÓS a junção e filtragem)
    # Usei groupby para calcular a diferença corretamente para cada país
    df_analysis_ready.sort_values(['entity', 'date'], inplace=True)
    df_analysis_ready['new_cases'] = df_analysis_ready.groupby('entity')['total_cases'].diff().fillna(0)
    
    # --- ETAPA 4: Selecionar países e realizar a análise ---
    PAIS_ANALISE = 'France'
    PAIS_COMPARACAO = 'Germany'

    df_main = df_analysis_ready[df_analysis_ready['entity'] == PAIS_ANALISE].copy()
    df_comp = df_analysis_ready[df_analysis_ready['entity'] == PAIS_COMPARACAO].copy()

    if df_main.empty:
        print(f"ERRO: Nenhum dado encontrado para o país principal '{PAIS_ANALISE}' após a junção. Tente outro país.")
        return

    print("Dados preparados com sucesso.\n")
    print(f"--- Análise de Estatística Descritiva ({PAIS_ANALISE}) ---")
    
    df_main.rename(columns={'value': 'icu_occupancy'}, inplace=True)
    desc_stats = df_main[['new_cases', 'icu_occupancy']].describe()
    print(desc_stats)
    
    # --- Geração de Gráficos ---
    fig, ax1 = plt.subplots(figsize=(14, 7))
    color = 'tab:blue'
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Novos Casos Diários', color=color)
    ax1.plot(df_main['date'], df_main['new_cases'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Ocupação Diária de UTI', color=color)
    ax2.plot(df_main['date'], df_main['icu_occupancy'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title(f'Evolução de Novos Casos e Ocupação de UTI em {PAIS_ANALISE}')
    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'series_temporais.png'))
    plt.close()
    print(f"\nGráfico 'series_temporais.png' salvo na pasta '{OUTPUT_DIR}'.")

    plt.figure(figsize=(10, 6))
    sns.histplot(df_main['icu_occupancy'].dropna(), kde=True, bins=30)
    plt.title(f'Distribuição da Ocupação Diária de UTI em {PAIS_ANALISE}')
    plt.xlabel('Número de Pacientes em UTI')
    plt.ylabel('Frequência')
    plt.savefig(os.path.join(OUTPUT_DIR, 'histograma_uti.png'))
    plt.close()
    print(f"Gráfico 'histograma_uti.png' salvo na pasta '{OUTPUT_DIR}'.\n")

    print(f"--- Análise de Correlação ({PAIS_ANALISE}) ---")
    correlation = df_main['new_cases'].corr(df_main['icu_occupancy'])
    print(f"Correlação de Pearson: {correlation:.4f}")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_main, x='new_cases', y='icu_occupancy', alpha=0.5)
    plt.title(f'Correlação entre Novos Casos e Ocupação de UTI em {PAIS_ANALISE}')
    plt.xlabel('Novos Casos Diários')
    plt.ylabel('Ocupação Diária de UTI')
    plt.savefig(os.path.join(OUTPUT_DIR, 'correlacao.png'))
    plt.close()
    print(f"Gráfico 'correlacao.png' salvo na pasta '{OUTPUT_DIR}'.\n")

    print(f"--- Teste de Hipótese: {PAIS_ANALISE} vs. {PAIS_COMPARACAO} ---")
    if df_comp.empty:
        print(f"AVISO: Nenhum dado encontrado para o país de comparação: '{PAIS_COMPARACAO}'.")
    else:
        icu_main = df_main['icu_occupancy'].dropna()
        icu_comp = df_comp['value'].dropna()
        print(f"Média de ocupação de UTI - {PAIS_ANALISE}: {icu_main.mean():.2f}")
        print(f"Média de ocupação de UTI - {PAIS_COMPARACAO}: {icu_comp.mean():.2f}")
        
        t_stat, p_value = ttest_ind(icu_main, icu_comp, equal_var=False)
        print(f"Estatística t: {t_stat:.4f}, P-valor: {p_value:.4f}")
        if p_value < 0.05:
            print("Conclusão: Rejeitamos a hipótese nula (diferença significativa).")
        else:
            print("Conclusão: Não rejeitamos a hipótese nula (sem diferença significativa).")
    print("\n")

    print(f"--- Análise de Probabilidade ({PAIS_ANALISE}) ---")
    percentil_75 = df_main['icu_occupancy'].quantile(0.75)
    dias_acima_limiar = df_main[df_main['icu_occupancy'] > percentil_75].shape[0]
    total_dias = df_main['icu_occupancy'].notna().sum()
    probabilidade = dias_acima_limiar / total_dias
    print(f"Probabilidade de a ocupação de UTI exceder {percentil_75:.2f}: {probabilidade:.2%}")

if __name__ == '__main__':
    run_analysis()
