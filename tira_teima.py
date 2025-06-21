# arquivo: tira_teima.py

import pandas as pd

def analisar_linhas_vazias(caminho_arquivo: str):
    """
    Função de diagnóstico para contar linhas com dados ausentes
    nas colunas 'director' e 'cast'.
    """
    print("\n" + "="*50)
    print("INICIANDO ANÁLISE DE DADOS AUSENTES (TIRA-TEIMA)")
    print("="*50)

    try:
        # Carrega o arquivo CSV
        df = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        print("Verifique se o caminho está correto e o arquivo está na pasta 'dados/'.")
        return

    # 1. Total de linhas no arquivo original
    total_linhas = len(df)
    print(f"Total de linhas no arquivo: {total_linhas}")

    # 2. Identifica as linhas onde 'director' ou 'cast' são nulos/vazios
    # O operador '|' (OU) garante que não contaremos a mesma linha duas vezes
    # se ambos os campos estiverem vazios.
    linhas_com_vazios = df[pd.isna(df['director']) | pd.isna(df['cast'])]
    
    num_linhas_com_vazios = len(linhas_com_vazios)

    # 3. Calcula as linhas que são efetivamente processadas pelo seu programa
    linhas_processadas = total_linhas - num_linhas_com_vazios
    
    print(f"Linhas onde 'director' está vazio: {df['director'].isna().sum()}")
    print(f"Linhas onde 'cast' está vazio: {df['cast'].isna().sum()}")
    
    print("\n--- Resultado do Tira-Teima ---")
    print(f"Total de linhas que serão IGNORADAS (director ou cast vazio): {num_linhas_com_vazios}")
    print(f"Total de linhas que serão PROCESSADAS pelo seu código: {linhas_processadas}")
    print("="*50)


# --- Execução do Script ---
if __name__ == "__main__":
    # Caminho para o arquivo de dados
    caminho_do_csv = 'dados/netflix_amazon_disney_titles.csv'
    analisar_linhas_vazias(caminho_do_csv)