# -*- coding: utf-8 -*-

class Grafo:
    """
    Implementação de uma estrutura de dados de grafo flexível.

    Esta classe utiliza uma representação por lista de adjacências e é capaz
    de modelar grafos direcionados ou não-direcionados, e ponderados.
    A lista de adjacências é implementada com um dicionário aninhado, onde cada
    vértice mapeia para um dicionário de seus vizinhos e os respectivos pesos das arestas.
    
    Seguindo os princípios de design para alto desempenho, o número de vértices e 
    arestas é mantido em atributos separados (`num_vertices` e `num_arestas`),
    garantindo que as operações de contagem sejam executadas em tempo constante O(1).
    """

    def __init__(self):
        """
        Construtor da classe Grafo.

        Inicializa um grafo vazio. A lista de adjacências é um dicionário vazio
        e os contadores de vértices e arestas são inicializados com zero.

        Complexidade de Tempo: O(1)
        """
        self.lista_adj = {}
        self.num_vertices = 0
        self.num_arestas = 0
        

    def obter_lista_adj(self):
        """
        Retorna o dicionário interno de adjacência.
        """
        return self.lista_adj


    def adicionar_vertice(self, vertice):
        """
        Adiciona um vértice ao grafo.

        Se o vértice já existir, nenhuma ação é tomada. Caso contrário, ele é
        adicionado ao grafo e o contador de vértices é incrementado.

        Args:
            vertice: O identificador do vértice (e.g., int, str).

        Returns:
            bool: True se o vértice foi adicionado, False caso contrário.

        Complexidade de Tempo: O(1) em média.
        """
        if vertice not in self.lista_adj:
            self.lista_adj[vertice] = {}  # O valor agora é um dicionário para os vizinhos ponderados
            self.num_vertices += 1
            return True
        return False

    def adicionar_aresta(self, u, v, peso=1, direcionado=False):
        """
        Adiciona uma aresta entre os vértices u e v.

        Esta função é flexível para grafos direcionados e não-direcionados.
        - Para grafos ponderados, se a aresta já existir, o peso é incrementado.
        - Para grafos não-direcionados, a aresta é adicionada nos dois sentidos.

        Args:
            u: O vértice de origem.
            v: O vértice de destino.
            peso (int, optional): O peso da aresta. Padrão é 1.
            direcionado (bool, optional): Se True, a aresta é apenas de u->v. 
                                         Se False, a aresta é u<->v. Padrão é False.

        Returns:
            bool: True se uma nova aresta foi criada, False caso contrário.
        """
        # Garante que ambos os vértices existam no grafo
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)

        # Adiciona a aresta u -> v
        if v not in self.lista_adj[u]:
            self.lista_adj[u][v] = peso
            self.num_arestas += 1
            nova_aresta = True
        else:
            # Se a aresta já existe, apenas incrementa o peso
            self.lista_adj[u][v] += peso
            nova_aresta = False

        # Se o grafo não for direcionado, adiciona a aresta v -> u
        if not direcionado:
            if u not in self.lista_adj[v]:
                self.lista_adj[v][u] = peso
            else:
                self.lista_adj[v][u] += peso
        
        return nova_aresta

    def obter_numero_vertices(self):
        """
        Retorna o número total de vértices no grafo.

        Returns:
            int: O número de vértices.

        Complexidade de Tempo: O(1).
        """
        return self.num_vertices

    def obter_numero_arestas(self):
        """
        Retorna o número total de arestas no grafo.

        Returns:
            int: O número de arestas.

        Complexidade de Tempo: O(1).
        """
        return self.num_arestas

    def obter_vertices(self):
        """
        Retorna uma lista com todos os vértices do grafo.

        Returns:
            list: Uma lista contendo todos os vértices.

        Complexidade de Tempo: O(|V|).
        """
        return list(self.lista_adj.keys())

    def obter_vizinhos(self, vertice):
        """
        Retorna os vizinhos de um dado vértice e os pesos das arestas.

        Args:
            vertice: O vértice cuja vizinhança é desejada.

        Returns:
            dict: Um dicionário mapeando vizinhos aos pesos das arestas.
                  Retorna um dicionário vazio se o vértice não existir.
        """
        return self.lista_adj.get(vertice, {})

    def __str__(self):
        """
        Retorna uma representação em string do grafo para visualização.

        Returns:
            str: A representação textual do grafo.

        Complexidade de Tempo: O(|V| + |E|).
        """
        if self.num_vertices == 0:
            return "Grafo Vazio"
        
        output = f"Grafo com {self.num_vertices} vértices e {self.num_arestas} arestas.\n"
        output += "Lista de Adjacências (Vértice -> {Vizinho: Peso}):\n"
        for vertice, vizinhos in self.lista_adj.items():
            output += f"  {vertice}: {vizinhos}\n"
        return output