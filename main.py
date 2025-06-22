# arquivo: main.py

import sys
from analise_rede.grafo import Grafo
from analise_rede.processador_dados import processar_arquivo
from analise_rede.algoritmos import (
    count_strongly_connected_components,
    count_connected_components,
    prim_mst_for_vertex,
    degree_centrality,
    closeness_centrality,
    approx_betweenness_centrality
)

def main():
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'
    #caminho_csv = 'TDE5 dataset/netflix_amazon_disney_titles.csv'

    # 1) Inicia grafos
    grafo_dir = Grafo()  # direcionado: ator -> diretor
    grafo_und = Grafo()  # não-direcionado: ator <-> ator

    processar_arquivo(caminho_csv, grafo_dir, grafo_und)

    # 2) Atividade 1: mostra vértices e arestas
    print("\n" + "="*60)
    print("RESULTADOS DA CONSTRUÇÃO DOS GRAFOS")
    print("="*60)
    print(f"Grafo Dir (V, E): {grafo_dir.obter_numero_vertices()}, {grafo_dir.obter_numero_arestas()}")
    print(f"Grafo Und (V, E): {grafo_und.obter_numero_vertices()}, {grafo_und.obter_numero_arestas()}")
    print("="*60)

    # 3) Atividade 2: componentes
    
    #scc = count_strongly_connected_components(grafo_dir.lista_adj)
    #cc  = count_connected_components    (grafo_und.lista_adj)
    #print(f"\nComponentes fortemente conexas: {scc}")
    #print(f"Componentes conexas:               {cc}")

# A função agora retorna (contagem, lista_de_tamanhos).
# Usamos '_' para indicar que vamos ignorar o segundo valor (a lista).
    scc_count, _ = count_strongly_connected_components(grafo_dir.lista_adj)
    cc_count, _  = count_connected_components(grafo_und.lista_adj)
    print(f"\nComponentes fortemente conexas: {scc_count}")
    print(f"Componentes conexas:               {cc_count}")

    # 4) Escolhe exemplos: um ator e um diretor
    exemplo_ator = next(iter(grafo_und.lista_adj))
    # extrai todos os diretores do grafo direcionado
    diretores = {v for nbrs in grafo_dir.lista_adj.values() for v in nbrs}
    exemplo_dir = next(iter(diretores))

    print(f"\nExemplo (Ator):    {exemplo_ator}")
    print(f"Exemplo (Diretor): {exemplo_dir}")

    # 5) Atividade 3: MST apenas no não-direcionado
    mst, custo = prim_mst_for_vertex(grafo_und.lista_adj, exemplo_ator)
    print(f"\nMST a partir de {exemplo_ator}: custo={custo}, arestas={len(mst)}")
    print(" Primeiras 10 arestas:")
    for u, v, p in mst[:10]:
        print(f"   {u} -- {v} (peso {p})")
    if len(mst) > 10:
        print(f"   ... e mais {len(mst) - 10} arestas")

    # 6) Atividade 4: Degree Centrality
    deg_dir = degree_centrality(grafo_dir.lista_adj, exemplo_dir, directed=True)
    deg_ato = degree_centrality(grafo_und.lista_adj, exemplo_ator, directed=False)
    print(f"\nDegree Centrality (Diretor): {deg_dir:.6f}")
    print(f"Degree Centrality (Ator):    {deg_ato:.6f}")

    # 7) Atividade 6: Closeness Centrality (rápido)
    clo_dir = closeness_centrality(grafo_dir.lista_adj, exemplo_dir)
    clo_ato = closeness_centrality(grafo_und.lista_adj, exemplo_ator)
    print(f"\nCloseness Centrality (Diretor): {clo_dir:.6f}")
    print(f"Closeness Centrality (Ator):    {clo_ato:.6f}")

    # 8) Atividade 5: Betweenness aproximado
    btw_dir = approx_betweenness_centrality(grafo_dir.lista_adj, exemplo_dir, k=100)
    btw_ato = approx_betweenness_centrality(grafo_und.lista_adj, exemplo_ator, k=100)
    print(f"\nBetweenness (apx) Diretor: {btw_dir:.6f}")
    print(f"Betweenness (apx) Ator:    {btw_ato:.6f}")

if __name__ == "__main__":
    main()
