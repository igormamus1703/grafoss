# arquivo: gerar_analise2.py

# --- Análise de Top 10 Diretores por Centralidade ---

import matplotlib.pyplot as plt
from analise_rede.grafo import Grafo
from analise_rede.processador_dados import processar_arquivo
from analise_rede.algoritmos import (
    top_betweenness_directors,
    top_closeness_directors,
)


def analisar_top_diretores_centralidade():
    """Análise dos diretores mais influentes por betweenness e closeness centrality."""
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'
    
    print("="*70)
    print("ANÁLISE DE TOP 10 DIRETORES POR CENTRALIDADE")
    print("="*70)
    
    print("\nCarregando grafos para análise de centralidade dos diretores...")
    grafo_dir = Grafo()
    grafo_und = Grafo()
    processar_arquivo(caminho_csv, grafo_dir, grafo_und)
    
    # Extrai todos os diretores do grafo direcionado
    diretores = {v for nbrs in grafo_dir.lista_adj.values() for v in nbrs}
    
    print(f"\nAnalisando {len(diretores)} diretores...")
    print(f"Grafo direcionado: {grafo_dir.obter_numero_vertices()} vértices, {grafo_dir.obter_numero_arestas()} arestas")
    
    # Análise por Betweenness Centrality
    print("\n" + "="*50)
    print("ANÁLISE POR BETWEENNESS CENTRALITY")
    print("="*50)
    print("Calculando top 10 diretores por Betweenness...")
    print("(Diretores que mais controlam o fluxo de informações na rede)")
    
    top_btw = top_betweenness_directors(grafo_dir.lista_adj, diretores, top_n=10, sample=100, seed=42, plot=True)
    
    print("\nTop 10 Diretores por Betweenness Centrality:")
    print("-" * 60)
    print(f"{'Pos.':<4} {'Diretor':<40} {'Betweenness':<15}")
    print("-" * 60)
    for rank, (nome, valor) in enumerate(top_btw, 1):
        print(f"{rank:<4} {nome:<40} {valor:.6f}")
    print("-" * 60)

    # Análise por Closeness Centrality
    print("\n" + "="*50)
    print("ANÁLISE POR CLOSENESS CENTRALITY")
    print("="*50)
    print("Calculando top 10 diretores por Closeness...")
    print("(Diretores que estão mais próximos de todos os outros na rede)")
    
    top_clo = top_closeness_directors(grafo_dir.lista_adj, diretores, top_n=10, plot=True)
    
    print("\nTop 10 Diretores por Closeness Centrality:")
    print("-" * 60)
    print(f"{'Pos.':<4} {'Diretor':<40} {'Closeness':<15}")
    print("-" * 60)
    for rank, (nome, valor) in enumerate(top_clo, 1):
        print(f"{rank:<4} {nome:<40} {valor:.6f}")
    print("-" * 60)
    
    # Análise comparativa
    print("\n" + "="*50)
    print("ANÁLISE COMPARATIVA")
    print("="*50)
    
    # Encontrar diretores que aparecem em ambos os rankings
    diretores_btw = {nome for nome, _ in top_btw}
    diretores_clo = {nome for nome, _ in top_clo}
    diretores_comuns = diretores_btw.intersection(diretores_clo)
    
    if diretores_comuns:
        print(f"\nDiretores que aparecem em AMBOS os rankings (Top 10):")
        for diretor in diretores_comuns:
            rank_btw = next(i for i, (nome, _) in enumerate(top_btw, 1) if nome == diretor)
            rank_clo = next(i for i, (nome, _) in enumerate(top_clo, 1) if nome == diretor)
            print(f"  • {diretor}: #{rank_btw} em Betweenness, #{rank_clo} em Closeness")
    else:
        print("\nNenhum diretor aparece em ambos os rankings Top 10.")
    
    # Estatísticas
    print(f"\nEstatísticas:")
    print(f"  • Total de diretores analisados: {len(diretores)}")
    print(f"  • Diretores únicos no Top 10 Betweenness: {len(diretores_btw)}")
    print(f"  • Diretores únicos no Top 10 Closeness: {len(diretores_clo)}")
    print(f"  • Diretores em ambos os rankings: {len(diretores_comuns)}")
    
    print("\n" + "="*70)
    print("ANÁLISE CONCLUÍDA!")
    print("="*70)


def analisar_diretor_especifico(nome_diretor):
    """Análise detalhada de um diretor específico."""
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'
    
    print(f"\nAnálise detalhada do diretor: {nome_diretor}")
    print("-" * 50)
    
    grafo_dir = Grafo()
    grafo_und = Grafo()
    processar_arquivo(caminho_csv, grafo_dir, grafo_und)
    
    if nome_diretor not in grafo_dir.lista_adj:
        print(f"Diretor '{nome_diretor}' não encontrado no dataset.")
        return
    
    # Calcular métricas para o diretor específico
    from analise_rede.algoritmos import (
        degree_centrality,
        closeness_centrality,
        approx_betweenness_centrality,
        in_degree_centrality
    )
    
    # Degree centrality
    deg = degree_centrality(grafo_dir.lista_adj, nome_diretor, directed=True)
    in_deg = in_degree_centrality(grafo_dir.lista_adj, nome_diretor)
    
    # Closeness centrality
    clo = closeness_centrality(grafo_dir.lista_adj, nome_diretor)
    
    # Betweenness centrality
    btw = approx_betweenness_centrality(grafo_dir.lista_adj, nome_diretor, k=100)
    
    print(f"Degree Centrality (Total): {deg:.6f}")
    print(f"In-Degree Centrality: {in_deg:.6f}")
    print(f"Closeness Centrality: {clo:.6f}")
    print(f"Betweenness Centrality: {btw:.6f}")
    
    # Número de atores que trabalharam com este diretor
    atores_que_trabalharam = len(grafo_dir.lista_adj.get(nome_diretor, {}))
    print(f"Número de atores que trabalharam com {nome_diretor}: {atores_que_trabalharam}")


if __name__ == "__main__":
    # Executar análise completa
    analisar_top_diretores_centralidade()
    
    # Exemplo de análise de diretor específico (descomente para usar)
    # analisar_diretor_especifico("Christopher Nolan")
