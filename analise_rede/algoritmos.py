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