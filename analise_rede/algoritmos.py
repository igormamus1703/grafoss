# -*- coding: utf-8 -*-
import heapq
import math
import random
from collections import deque

def count_strongly_connected_components(graph):
    """Conta SCCs e retorna a contagem e a distribuição de seus tamanhos."""
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    scc_count = 0  # Antes
    scc_sizes = [] # Para guardar os tamanhos

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, {}):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            component_size = 0
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component_size += 1
                if w == v:
                    break
            scc_sizes.append(component_size)

    for v in graph:
        if v not in indices:
            strongconnect(v)
    # retornar uma tupla com dois valores
    # return scc_count # Linha original para execução do main.py
    return len(scc_sizes), scc_sizes


def count_connected_components(graph):
    """Conta componentes conexas e retorna a contagem e a distribuição de seus tamanhos."""
    visited = set()
    component_sizes = []
    for v in graph:
        if v not in visited:
            component_size = 0
            stack = [v]
            visited.add(v)
            component_size += 1
            while stack:
                u = stack.pop()
                for w in graph.get(u, {}):
                    if w not in visited:
                        visited.add(w)
                        stack.append(w)
                        component_size += 1
            component_sizes.append(component_size)
    #retornar uma tupla com dois valores
    # return count # Linha original para execução do main.py
    return len(component_sizes), component_sizes


def prim_mst_for_vertex(graph, X):
    """Retorna (lista_de_arestas, custo_total) da MST da componente de X."""
    if X not in graph:
        raise ValueError(f"Vértice {X} não existe no grafo.")
    
    # Primeiro, encontra todos os vértices na mesma componente
    visited = set()
    component_vertices = set()
    stack = [X]
    visited.add(X)
    
    while stack:
        u = stack.pop()
        component_vertices.add(u)
        for v in graph.get(u, {}):
            if v not in visited:
                visited.add(v)
                stack.append(v)
    
    # Agora executa Prim apenas na componente
    if len(component_vertices) <= 1:
        return [], 0
    
    visited_mst = {X}
    mst_edges = []
    total_cost = 0
    heap = [(peso, X, neigh) for neigh, peso in graph[X].items() if neigh in component_vertices]
    heapq.heapify(heap)

    while heap and len(visited_mst) < len(component_vertices):
        peso, u, v = heapq.heappop(heap)
        if v in visited_mst:
            continue
        visited_mst.add(v)
        mst_edges.append((u, v, peso))
        total_cost += peso
        for neigh, w in graph[v].items():
            if neigh in component_vertices and neigh not in visited_mst:
                heapq.heappush(heap, (w, v, neigh))

    return mst_edges, total_cost


def degree_centrality(graph, v, directed=False):
    """
    Centralidade de grau normalizada de v (0–1).
    - directed=False -> grau(v) / (N-1)
    - directed=True  -> (in-degree(v) + out-degree(v)) / (2*(N-1))
    """
    if v not in graph:
        raise ValueError(f"Vértice {v} não existe no grafo.")

    N = len(graph)
    if N <= 1:
        return 0.0

    grau = len(graph[v])
    if directed:
        grau += sum(1 for nbrs in graph.values() if v in nbrs)
        return grau / (2 * (N - 1))

    return grau / (N - 1)


def betweenness_centrality(graph, v):
    """Centralidade de intermediação normalizada de v (0–1), versão otimizada."""
    if v not in graph:
        raise ValueError(f"Vértice {v} não existe no grafo.")
    
    N = len(graph)
    if N <= 2:
        return 0.0
    
    betw = 0.0
    nodes = list(graph.keys())
    
    # Para grafos muito grandes, limitamos o número de vértices fonte
    max_sources = min(100, N)  # Limita a 100 vértices fonte para performance
    
    for s in nodes[:max_sources]:
        if s == v:
            continue
            
        # BFS para caminhos mais curtos (sem pesos)
        queue = deque([s])
        dist = {u: float('inf') for u in graph}
        dist[s] = 0
        sigma = {u: 0 for u in graph}
        sigma[s] = 1
        P = {u: [] for u in graph}
        
        while queue:
            u = queue.popleft()
            for w in graph[u]:
                if dist[w] == float('inf'):
                    dist[w] = dist[u] + 1
                    queue.append(w)
                if dist[w] == dist[u] + 1:
                    sigma[w] += sigma[u]
                    P[w].append(u)
        
        # Acumula dependências
        delta = {u: 0.0 for u in graph}
        stack = [u for u in graph if dist[u] != float('inf')]
        stack.sort(key=lambda x: dist[x], reverse=True)
        
        for w in stack:
            for u in P[w]:
                delta[u] += (sigma[u] / sigma[w]) * (1 + delta[w])
            if w != s:
                betw += delta[w]
    
    # Normalização
    if max_sources < N:
        # Ajusta para o número total de vértices
        betw = betw * (N / max_sources)
    
    # Detecta se é não-direcionado
    undirected = all(u in graph[w] for u in graph for w in graph[u])
    if undirected:
        betw /= 2.0
    
    # Normalização final
    norm = (N - 1) * (N - 2)
    if undirected:
        norm /= 2.0
    
    return betw / norm if norm > 0 else 0.0


def closeness_centrality(graph, v):
    """Centralidade de proximidade normalizada de ``v`` em ``[0, 1]``."""
    if v not in graph:
        raise ValueError(f"Vértice {v} não existe no grafo.")

    N = len(graph)
    if N <= 1:
        return 0.0

    # BFS não ponderado para obter distâncias mínimas
    dist = {u: -1 for u in graph}
    dist[v] = 0
    queue = deque([v])
    reachable = 1

    while queue:
        u = queue.popleft()
        for w in graph[u]:
            if dist[w] == -1:
                dist[w] = dist[u] + 1
                queue.append(w)
                reachable += 1

    total_dist = sum(d for d in dist.values() if d > 0)
    if total_dist <= 0:
        return 0.0

    closeness = (reachable - 1) / total_dist
    if reachable < N:
        closeness *= (reachable - 1) / (N - 1)

    return closeness


def approx_betweenness_centrality(graph, v, k=50, seed=42):
    """
    Estima Betweenness Centrality de v amostrando k fontes (BFS não-ponderado).
    Retorna valor entre 0 e 1.
    """
    if v not in graph:
        raise ValueError(f"Vértice {v} não existe no grafo.")
    nodes = list(graph.keys())
    N = len(nodes)
    if N < 3:
        return 0.0

    random.seed(seed)
    fontes = random.sample(nodes, min(k, N))
    accum = 0.0

    for s in fontes:
        if s == v:
            continue
        # Brandes simplificado para apenas acumular delta[v] em BFS não-ponderado
        dist = {u: -1 for u in graph}
        sigma = {u: 0 for u in graph}
        P = {u: [] for u in graph}
        dist[s] = 0
        sigma[s] = 1
        queue = deque([s])
        order = []

        while queue:
            u = queue.popleft()
            order.append(u)
            for w in graph[u]:
                # descoberta
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    queue.append(w)
                # caminho mínimo
                if dist[w] == dist[u] + 1:
                    sigma[w] += sigma[u]
                    P[w].append(u)

        delta = {u: 0.0 for u in graph}
        for w in reversed(order):
            for u in P[w]:
                delta[u] += (sigma[u] / sigma[w]) * (1 + delta[w])
        accum += delta[v]

    # normalização: cada par (s,t) contado uma vez
    # fator = k * (N-1)*(N-2)/2   → queremos fracasso sobre total de pares possíveis
    norm = (N - 1) * (N - 2) / 2
    return (accum * N / len(fontes)) / norm


def approx_betweenness_centrality_all(graph, k=50, seed=42):
    """Estimativa da betweenness de todos os vértices usando amostragem."""
    nodes = list(graph.keys())
    N = len(nodes)
    if N < 3:
        return {v: 0.0 for v in nodes}

    random.seed(seed)
    fontes = random.sample(nodes, min(k, N))
    betw = {v: 0.0 for v in nodes}

    undirected = all(u in graph[w] for u in graph for w in graph[u])

    for s in fontes:
        dist = {v: -1 for v in nodes}
        sigma = {v: 0 for v in nodes}
        P = {v: [] for v in nodes}
        dist[s] = 0
        sigma[s] = 1
        queue = deque([s])
        order = []

        while queue:
            v = queue.popleft()
            order.append(v)
            for w in graph[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)

        delta = {v: 0.0 for v in nodes}
        for w in reversed(order):
            for u in P[w]:
                delta[u] += (sigma[u] / sigma[w]) * (1 + delta[w])
            if w != s:
                betw[w] += delta[w]

    norm = (N - 1) * (N - 2)
    if undirected:
        norm /= 2.0

    scale = (N / len(fontes)) / norm
    for v in betw:
        betw[v] *= scale
    return betw


def _plot_bar_chart(pares, titulo):
    """Função auxiliar para plotar gráficos de barras horizontais."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib não está disponível. Gráfico não será exibido.")
        return

    nomes = [p[0] for p in pares]
    valores = [p[1] for p in pares]
    plt.figure(figsize=(10, 6))
    plt.barh(nomes[::-1], valores[::-1])
    plt.xlabel("Centralidade")
    plt.title(titulo)
    plt.tight_layout()
    plt.show()

#questao 4 do relatorio
def top_betweenness_directors(graph, diretores, top_n=10, sample=50, seed=42, plot=True):
    """Retorna e opcionalmente plota os diretores mais centrais por betweenness."""
    bc_all = approx_betweenness_centrality_all(graph, k=sample, seed=seed)
    filtrado = {d: bc_all.get(d, 0.0) for d in diretores}
    ordenado = sorted(filtrado.items(), key=lambda x: x[1], reverse=True)[:top_n]
    if plot:
        _plot_bar_chart(ordenado, "Top Betweenness Centrality (Diretores)")
    return ordenado

#questao 5 do relatorio
def top_closeness_directors(graph, diretores, top_n=10, plot=True):
    """Retorna e opcionalmente plota os diretores mais centrais por closeness."""
    cc = {d: closeness_centrality(graph, d) for d in diretores if d in graph}
    ordenado = sorted(cc.items(), key=lambda x: x[1], reverse=True)[:top_n]
    if plot:
        _plot_bar_chart(ordenado, "Top Closeness Centrality (Diretores)")
    return ordenado


#Para a questão 3 do relatório
def in_degree_centrality(graph, v):
    """Calcula a centralidade de grau de entrada (in-degree) normalizada."""
    if v not in graph:
        return 0.0

    N = len(graph)
    if N <= 1:
        return 0.0

    in_degree = 0
    # Itera em todos os nós para ver quem aponta para 'v'
    for node in graph:
        if v in graph[node]:
            in_degree += 1

    # Normaliza pelo número máximo de arestas de entrada possíveis (N-1)
    return in_degree / (N - 1)

def calcular_centralidades_de_grau_em_lote(grafo):
    """
    Calcula a Centralidade de Grau para TODOS os vértices de um grafo de uma só vez.

    Esta função é uma otimização para evitar chamar a função de centralidade
    individual milhares de vezes.

    Args:
        grafo (Grafo): O objeto de grafo a ser analisado.

    Returns:
        dict: Um dicionário mapeando cada vértice à sua centralidade de grau normalizada.
    """
    centralidades = {}
    num_vertices = grafo.obter_numero_vertices()

    if num_vertices <= 1:
        return {}

    denominador = float(num_vertices - 1)

    # Itera sobre todos os vértices para calcular a centralidade de cada um
    for vertice in grafo.obter_vertices():
        # O grau é o número de vizinhos
        grau = len(grafo.obter_vizinhos(vertice))
        centralidades[vertice] = grau / denominador
        
    return centralidades

def calcular_centralidades_de_intermediacao_aprox(grafo, k=100, semente=42):
    """
    Calcula uma aproximação da Centralidade de Intermediação para todos os nós.

    O algoritmo seleciona uma amostra de 'k' vértices e calcula os caminhos
    mais curtos a partir deles, extrapolando o resultado para toda a rede.
    Isso torna o cálculo viável para grafos grandes.

    Args:
        grafo (Grafo): O objeto de grafo a ser analisado.
        k (int): O número de nós a serem usados como amostra. Um 'k' maior
                 aumenta a precisão, mas também o tempo de execução.
        semente (int): Semente para o gerador de números aleatórios para
                     garantir que a amostra seja a mesma em diferentes execuções.

    Returns:
        dict: Um dicionário mapeando cada vértice à sua centralidade de 
              intermediação aproximada e normalizada.
    """
    random.seed(semente)
    vertices = grafo.obter_vertices()
    num_vertices = len(vertices)
    
    # Seleciona uma amostra de k vértices para usar como fontes
    if k > num_vertices:
        fontes = vertices
    else:
        fontes = random.sample(vertices, k)
    
    intermediacao = {v: 0.0 for v in vertices}

    for s in fontes:
        # Etapa 1: BFS para encontrar caminhos mais curtos
        pilha = []
        predecessores = {v: [] for v in vertices}
        sigma = {v: 0.0 for v in vertices}
        sigma[s] = 1.0
        distancia = {v: -1 for v in vertices}
        distancia[s] = 0
        fila = deque([s])

        while fila:
            v = fila.popleft()
            pilha.append(v)

            for w in grafo.obter_vizinhos(v):
                if distancia[w] < 0:
                    fila.append(w)
                    distancia[w] = distancia[v] + 1
                
                if distancia[w] == distancia[v] + 1:
                    sigma[w] += sigma[v]
                    predecessores[w].append(v)
        
        # Etapa 2: Acumular dependências
        delta = {v: 0.0 for v in vertices}
        while pilha:
            w = pilha.pop()
            for v_pred in predecessores[w]:
                # O fator de divisão sigma[w] não pode ser zero
                if sigma[w] != 0:
                    fator = (sigma[v_pred] / sigma[w])
                    delta[v_pred] += fator * (1 + delta[w])
            
            if w != s:
                intermediacao[w] += delta[w]

    # Normalização final
    if num_vertices > 2:
        # Fator de escala pela amostragem
        fator_escala = num_vertices / k
        # Normalizador para grafos não-direcionados
        normalizador = (num_vertices - 1) * (num_vertices - 2) / 2.0
        for v in intermediacao:
            intermediacao[v] = (intermediacao[v] * fator_escala) / normalizador
    
    return intermediacao

def calcular_centralidades_de_proximidade_em_lote(grafo):
    """
    Calcula a Centralidade de Proximidade para todos os vértices de um grafo.

    A função lida corretamente com grafos não-conectados, calculando a 
    centralidade dentro da componente de cada nó e normalizando pelo tamanho
    total da rede (Fórmula de Wasserman e Faust).

    Args:
        grafo (Grafo): O objeto de grafo a ser analisado.

    Returns:
        dict: Um dicionário mapeando cada vértice à sua centralidade de proximidade.
    """
    centralidades = {}
    todos_os_vertices = grafo.obter_vertices()
    num_vertices_total = len(todos_os_vertices)

    if num_vertices_total <= 1:
        return {}
    
    print("Iniciando cálculo exato de Centralidade de Proximidade...")
    
    # Loop principal que executa a BFS para cada nó
    for i, vertice in enumerate(todos_os_vertices):
        # --- Indicador de Progresso ---
        # Imprime o progresso na mesma linha para não poluir o console
        progresso = (i + 1) / num_vertices_total * 100
        print(f"\rCalculando... {progresso:.2f}% concluído ({i+1}/{num_vertices_total})", end="")

        # Etapa 1: BFS para encontrar distâncias a partir do 'vertice' atual
        distancia = {vertice: 0}
        fila = deque([vertice])
        soma_distancias = 0
        
        while fila:
            u = fila.popleft()
            soma_distancias += distancia[u]
            
            for v_vizinho in grafo.obter_vizinhos(u):
                if v_vizinho not in distancia:
                    distancia[v_vizinho] = distancia[u] + 1
                    fila.append(v_vizinho)
        
        # Etapa 2: Cálculo da centralidade para o 'vertice'
        num_alcalcaveis = len(distancia)
        
        if soma_distancias == 0 or num_alcalcaveis <= 1:
            centralidades[vertice] = 0.0
            continue

        # Fórmula de Wasserman e Faust para grafos não-conectados/direcionados
        fator_alcance = (num_alcalcaveis - 1) / (num_vertices_total - 1)
        proximidade_bruta = (num_alcalcaveis - 1) / soma_distancias
        
        centralidades[vertice] = proximidade_bruta * fator_alcance

    print("\nCálculo de Proximidade finalizado.")
    return centralidades

def calcular_centralidades_de_proximidade_aprox(grafo, k=200, semente=42):
    """
    Calcula uma aproximação da Centralidade de Proximidade para todos os nós.

    Seleciona uma amostra de 'k' nós pivô e calcula a soma das distâncias de
    todos os outros nós para essa amostra, tornando o cálculo viável.

    Args:
        grafo (Grafo): O objeto de grafo a ser analisado.
        k (int): O número de nós pivô a serem usados na amostragem.
        semente (int): Semente para reprodutibilidade.

    Returns:
        dict: Um dicionário mapeando cada vértice à sua centralidade de 
              proximidade aproximada e normalizada.
    """
    random.seed(semente)
    vertices = grafo.obter_vertices()
    num_vertices_total = len(vertices)

    if num_vertices_total <= 1:
        return {}

    # Seleciona k nós pivô aleatoriamente
    pivos = random.sample(vertices, min(k, num_vertices_total))
    
    soma_distancias = {v: 0.0 for v in vertices}
    
    # Executa uma BFS a partir de cada pivô
    for pivo in pivos:
        distancia = {pivo: 0}
        fila = deque([pivo])
        
        while fila:
            u = fila.popleft()
            for v_vizinho in grafo.obter_vizinhos(u):
                if v_vizinho not in distancia:
                    distancia[v_vizinho] = distancia[u] + 1
                    fila.append(v_vizinho)
        
        # Adiciona a distância encontrada à soma de cada nó
        for v in vertices:
            if v in distancia:
                soma_distancias[v] += distancia[v]

    # Calcula a centralidade aproximada para cada vértice
    centralidades = {}
    for v in vertices:
        if soma_distancias[v] == 0:
            centralidades[v] = 0.0
        else:
            # A centralidade é o inverso da distância média para os pivôs
            centralidade_aprox = k / soma_distancias[v]
            centralidades[v] = centralidade_aprox

    return centralidades