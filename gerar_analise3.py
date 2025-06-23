from analise_rede.grafo import Grafo
from analise_rede.processador_dados import processar_arquivo
# Importamos a nova função de cálculo em lote
from analise_rede.algoritmos import calcular_centralidades_de_grau_em_lote, calcular_centralidades_de_intermediacao_aprox, calcular_centralidades_de_proximidade_em_lote, calcular_centralidades_de_proximidade_aprox 

def analisar_atividade_6(grafo_nao_direcionado):
    """
    Executa a análise completa para a Atividade 6 do TDE.
    """
    print("\n" + "="*70)
    print("INICIANDO ANÁLISE DA ATIVIDADE 6")
    print("Top 10 Atores/Atrizes por Centralidade de Grau")
    print("="*70)

    # 1. Calcula a centralidade para todos os atores usando a função em lote
    centralidade_grau = calcular_centralidades_de_grau_em_lote(grafo_nao_direcionado)
    
    # 2. Ordena os resultados para encontrar o Top 10
    atores_ordenados = sorted(
        centralidade_grau.items(), 
        key=lambda item: item[1], 
        reverse=True
    )
    
    top_10_atores = atores_ordenados[:10]

    # 3. Apresenta os resultados em uma tabela
    print("\nResultado: Os 10 atores/atrizes mais influentes por Centralidade de Grau são:\n")
    print("-" * 65)
    print(f"{'Posição':<10} {'Ator/Atriz':<40} {'Centralidade (Normalizada)':<25}")
    print("-" * 65)
    for i, (ator, centralidade) in enumerate(top_10_atores):
        print(f"{i+1:<10} {ator:<40} {centralidade:<25.6f}")
    print("-" * 65)

 

def analisar_atividade_7(grafo_nao_direcionado):
    """
    Executa a análise completa para a Atividade 7 do TDE.
    """
    print("\n" + "="*70)
    print("INICIANDO ANÁLISE DA ATIVIDADE 7")
    print("Top 10 Atores/Atrizes por Centralidade de Intermediação")
    print("="*70)
    print("Atenção: Este cálculo é uma aproximação e pode levar alguns minutos...")

    # 1. Calcula a centralidade de intermediação aproximada
    centralidade_interm = calcular_centralidades_de_intermediacao_aprox(grafo_nao_direcionado, k=200) # Aumentar 'k' para mais precisão
    
    # 2. Ordena os resultados para encontrar o Top 10
    atores_ordenados = sorted(centralidade_interm.items(), key=lambda item: item[1], reverse=True)
    top_10_atores = atores_ordenados[:10]

    # 3. Apresenta os resultados em uma tabela
    print("\nResultado: Os 10 atores/atrizes mais influentes por Centralidade de Intermediação são:\n")
    print("-" * 65)
    print(f"{'Posição':<10} {'Ator/Atriz':<40} {'Centralidade (Aproximada)':<25}")
    print("-" * 65)
    for i, (ator, centralidade) in enumerate(top_10_atores):
        print(f"{i+1:<10} {ator:<40} {centralidade:<25.6f}")
    print("-" * 65)




def analisar_atividade_8_aprox(grafo_nao_direcionado):
    """
    Executa a análise da Atividade 8 usando a aproximação.
    """
    print("\n" + "="*70)
    print("INICIANDO ANÁLISE DA ATIVIDADE 8 (CÁLCULO APROXIMADO)")
    print("Top 10 Atores/Atrizes por Centralidade de Proximidade")
    print("="*70)

    # 1. Calcula a centralidade de proximidade aproximada
    centralidade_prox = calcular_centralidades_de_proximidade_em_lote(grafo_nao_direcionado)
    
    # 2. Ordena e pega o Top 10
    atores_ordenados = sorted(centralidade_prox.items(), key=lambda item: item[1], reverse=True)
    top_10_atores = atores_ordenados[:10]

    # 3. Apresenta os resultados
    print("\nResultado: Os 10 atores/atrizes mais influentes por Centralidade de Proximidade (Aproximada) são:\n")
    print("-" * 65)
    print(f"{'Posição':<10} {'Ator/Atriz':<40} {'Centralidade (Aproximada)':<25}")
    print("-" * 65)
    for i, (ator, centralidade) in enumerate(top_10_atores):
        print(f"{i+1:<10} {ator:<40} {centralidade:<25.6f}")
    print("-" * 65)






def main():
    """
    Função principal para executar as análises de métricas.
    """
    print("Construindo grafos... Por favor, aguarde.")
    caminho_csv = 'dados/netflix_amazon_disney_titles.csv'
    grafo_ator_diretor = Grafo()
    grafo_ator_ator = Grafo()
    processar_arquivo(caminho_csv, grafo_ator_diretor, grafo_ator_ator)
    print("Grafos construídos com sucesso!")

    # Executa a análise específica da Atividade 6
    analisar_atividade_6(grafo_ator_ator)
    analisar_atividade_7(grafo_ator_ator)
    analisar_atividade_8_aprox(grafo_ator_ator)


if __name__ == "__main__":
    main()