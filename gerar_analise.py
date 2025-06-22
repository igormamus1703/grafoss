# arquivo: gerar_analise.py

# --- Código para gerar análise do relatório ---


# pip install matplotlib tqdm
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from analise_rede.grafo import Grafo
from analise_rede.processador_dados import processar_arquivo
from analise_rede.algoritmos import degree_centrality
from analise_rede.algoritmos import count_connected_components, count_strongly_connected_components
from analise_rede.algoritmos import in_degree_centrality

def analisar_distribuicao_graus():
    """
    Calcula a centralidade de grau para todos os nós e gera histogramas.
    """
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'

    print("Carregando e processando os grafos...")
    grafo_dir = Grafo()
    grafo_und = Grafo()
    processar_arquivo(caminho_csv, grafo_dir, grafo_und)
    print("Grafos carregados.")

    # --- Grafo Não-Direcionado (Atores) ---
    print("\nCalculando distribuição de grau para o grafo de Atores...")
    graus_atores = [
        degree_centrality(grafo_und.lista_adj, ator) 
        for ator in tqdm(grafo_und.obter_vertices(), desc="Atores")
    ]

    # --- Grafo Direcionado (Atores e Diretores) ---
    print("\nCalculando distribuição de grau para o grafo Atores-Diretores...")
    graus_dir = [
        degree_centrality(grafo_dir.lista_adj, no, directed=True) 
        for no in tqdm(grafo_dir.obter_vertices(), desc="Atores/Diretores")
    ]

    print("\nCálculos finalizados. Gerando gráficos...")

    plt.figure(figsize=(15, 7))

    plt.subplot(1, 2, 1)
    plt.hist(graus_atores, bins=50, color='royalblue', alpha=0.8)
    plt.title('Distribuição de Grau - Atores (Não-Direcionado)')
    plt.xlabel('Centralidade de Grau')
    plt.ylabel('Frequência (Nº de Atores)')
    plt.yscale('log')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.subplot(1, 2, 2)
    plt.hist(graus_dir, bins=50, color='seagreen', alpha=0.8)
    plt.title('Distribuição de Grau - Atores/Diretores (Direcionado)')
    plt.xlabel('Centralidade de Grau (Grau de Saída)')
    plt.ylabel('Frequência (Nº de Nós)')
    plt.yscale('log')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('distribuicao_graus.png')
    print("\nGráfico 'distribuicao_graus.png' salvo na pasta do projeto!")
    plt.show()

def analisar_distribuicao_componentes():
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'
    print("\nCarregando grafos para análise de componentes...")
    grafo_dir = Grafo()
    grafo_und = Grafo()
    processar_arquivo(caminho_csv, grafo_dir, grafo_und)

    # Análise do Grafo Não-Direcionado
    num_cc, tamanhos_cc = count_connected_components(grafo_und.lista_adj)
    print(f"\nGrafo Não-Direcionado (Atores):")
    print(f"  - Número total de Componentes Conexas: {num_cc}")
    if tamanhos_cc:
        print(f"  - Tamanho da maior componente (gigante): {max(tamanhos_cc)}")
    
    # Análise do Grafo Direcionado
    num_scc, tamanhos_scc = count_strongly_connected_components(grafo_dir.lista_adj)
    print(f"\nGrafo Direcionado (Atores-Diretores):")
    print(f"  - Número total de Componentes Fortemente Conexas: {num_scc}")
    if tamanhos_scc:
        print(f"  - Tamanho da maior componente: {max(tamanhos_scc)}")

    # --- Gráficos com Rótulos ---
    plt.figure(figsize=(16, 8))

    # Gráfico 1: Componentes Conexas
    ax1 = plt.subplot(1, 2, 1)
    # A função hist retorna as contagens (n) e as barras (patches)
    n, bins, patches = ax1.hist(tamanhos_cc, bins=50, color='coral', alpha=0.8)
    ax1.set_title('Distribuição de Tamanho - Componentes Conexas')
    ax1.set_xlabel('Tamanho da Componente (Nº de Vértices)')
    ax1.set_ylabel('Frequência')
    ax1.set_yscale('log')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # --- Laço para adicionar os rótulos ---
    for i, patch in enumerate(patches):
        height = patch.get_height()
        # Adiciona o rótulo apenas se a barra for significativa, para não poluir
        if height > 0 and n[i] > 1: # Mostra valores acima de 1
            ax1.text(patch.get_x() + patch.get_width() / 2, height, f'{int(n[i])}', 
                     ha='center', va='bottom', fontsize=8, rotation=90)


    # Gráfico 2: Componentes Fortemente Conexas
    ax2 = plt.subplot(1, 2, 2)
    n, bins, patches = ax2.hist(tamanhos_scc, bins=50, color='purple', alpha=0.8)
    ax2.set_title('Distribuição de Tamanho - Comp. Fortemente Conexas')
    ax2.set_xlabel('Tamanho da Componente (Nº de Vértices)')
    ax2.set_ylabel('Frequência')
    ax2.set_yscale('log')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # ---Laço para adicionar os rótulos ---
    for i, patch in enumerate(patches):
        height = patch.get_height()
        if height > 0:
            ax2.text(patch.get_x() + patch.get_width() / 2, height, f'{int(n[i])}', 
                     ha='center', va='bottom', fontsize=9)


    plt.tight_layout()
    plt.savefig('distribuicao_componentes_com_valores.png')
    print("\nGráfico 'distribuicao_componentes_com_valores.png' salvo!")
    plt.show()

def analisar_top_diretores_por_grau():
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'
    print("\nCarregando grafos para análise de Top 10 Diretores...")
    grafo_dir = Grafo()
    # O grafo não-direcionado é útil para separar quem são os atores
    grafo_und = Grafo()
    processar_arquivo(caminho_csv, grafo_dir, grafo_und)

    # 1. Identificar os nós que são primariamente diretores
    todos_os_nos = set(grafo_dir.obter_vertices())
    atores = set(grafo_und.obter_vertices())
    # Consideramos diretores todos que aparecem na coluna 'director'.
    # Para uma lista mais pura, pegamos nós que não são atores no grafo de atores.
    diretores = list(todos_os_nos - atores) 

    print(f"\nCalculando Grau de Entrada para {len(diretores)} diretores...")

    # 2. Calcular o grau de entrada para cada diretor
    ranking_diretores = []
    for diretor in tqdm(diretores, desc="Ranking Diretores"):
        # Usamos a nova função de in-degree
        grau_entrada = in_degree_centrality(grafo_dir.lista_adj, diretor)
        if grau_entrada > 0:
            ranking_diretores.append((diretor, grau_entrada))

    # 3. Ordenar e pegar o Top 10
    ranking_diretores.sort(key=lambda item: item[1], reverse=True)

    print("\n--- TOP 10 DIRETORES MAIS INFLUENTES (POR GRAU DE ENTRADA) ---")
    print("-" * 65)
    print(f"{'Pos.':<5} {'Diretor':<45} {'Centralidade de Grau (Normalizada)':<20}")
    print("-" * 65)
    for i, (diretor, grau) in enumerate(ranking_diretores[:10]):
        print(f"{i+1:<5} {diretor:<45} {grau:.6f}")
    print("-" * 65)


if __name__ == "__main__":
    # analisar_distribuicao_graus()  # Questão 1
    #analisar_distribuicao_componentes()  # Questão 2
    analisar_top_diretores_por_grau() # Questão 3
