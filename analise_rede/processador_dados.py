# arquivo: analise_rede/processador_dados.py

import pandas as pd
from .grafo import Grafo # Usamos o '.' para indicar importação dentro do mesmo pacote

def limpar_string(nome: str) -> str:
    """Padroniza os nomes: maiúsculas e sem espaços extras."""
    return nome.strip().upper()

def processar_arquivo(caminho_arquivo: str, grafo_direcionado: Grafo, grafo_nao_direcionado: Grafo):
    """
    Lê o arquivo CSV e popula ambos os grafos.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.
        grafo_direcionado (Grafo): Instância do grafo direcionado (Ator -> Diretor) a ser populada.
        grafo_nao_direcionado (Grafo): Instância do grafo não-direcionado (Ator <-> Ator) a ser populada.
    """
    print("Iniciando o processamento do arquivo CSV...")

    # Carrega o CSV usando pandas.
    df = pd.read_csv(caminho_arquivo)

    # Remove linhas onde 'director' ou 'cast' são vazios, conforme solicitado.
    df.dropna(subset=['director', 'cast'], inplace=True)

    # Itera sobre cada linha (cada obra do catálogo)
    for _, linha in df.iterrows():
        # Extrai e limpa a lista de diretores e do elenco da obra atual
        diretores_brutos = linha['director'].split(',')
        elenco_brutos = linha['cast'].split(',')
        
        diretores = [limpar_string(d) for d in diretores_brutos]
        elenco = [limpar_string(a) for a in elenco_brutos]

        # --- Populando o Grafo Direcionado (Ator -> Diretor) --- 
        # Para cada ator e cada diretor na mesma obra, cria a relação ponderada.
        for ator in elenco:
            for diretor in diretores:
                # A aresta é direcionada do ator para o diretor
                grafo_direcionado.adicionar_aresta(ator, diretor, peso=1, direcionado=True)

        # --- Populando o Grafo Não-Direcionado (Ator <-> Ator) --- 
        # Gera todos os pares únicos de atores no mesmo elenco para criar as arestas.
        # O laço começa com j = i + 1 para evitar arestas de um ator com ele mesmo e duplicatas.
        for i in range(len(elenco)):
            for j in range(i + 1, len(elenco)):
                ator1 = elenco[i]
                ator2 = elenco[j]
                # A aresta é não-direcionada (padrão do método)
                grafo_nao_direcionado.adicionar_aresta(ator1, ator2, peso=1)

    print("Processamento do arquivo finalizado.")