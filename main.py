# arquivo: main.py

from analise_rede.grafo import Grafo
from analise_rede.processador_dados import processar_arquivo

def main():
    # Caminho para o arquivo de dados
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'

    # Cria as instâncias dos dois grafos solicitados
    grafo_ator_diretor = Grafo() # Grafo ponderado direcionado 
    grafo_ator_ator = Grafo()     # Grafo ponderado não-direcionado 

    # Processa o arquivo e popula ambos os grafos de uma só vez
    processar_arquivo(caminho_csv, grafo_ator_diretor, grafo_ator_ator)

    # --- Exibição dos Resultados da Atividade 1 --- 
    print("\n" + "="*50)
    print("RESULTADOS DA CONSTRUÇÃO DOS GRAFOS")
    print("="*50)

    print("\n--- Grafo Direcionado (Ator -> Diretor) ---")
    print(f"  - Quantidade de Vértices: {grafo_ator_diretor.obter_numero_vertices()}")
    print(f"  - Quantidade de Arestas: {grafo_ator_diretor.obter_numero_arestas()}")

    print("\n--- Grafo Não-Direcionado (Ator <-> Ator) ---")
    print(f"  - Quantidade de Vértices: {grafo_ator_ator.obter_numero_vertices()}")
    print(f"  - Quantidade de Arestas: {grafo_ator_ator.obter_numero_arestas()}")
    print("\n" + "="*50)


if __name__ == "__main__":
    main()