# -*- coding: utf-8 -*-

class Grafo:
    

    def __init__(self):
  
        self.lista_adj = {}
        self.num_vertices = 0
        self.num_arestas = 0
        

    def obter_lista_adj(self):

        #Retorna o dicionário interno de adjacência.
        return self.lista_adj

    def adicionar_vertice(self, vertice):

        if vertice not in self.lista_adj:
            self.lista_adj[vertice] = {}  # O valor agora é um dicionário para os vizinhos ponderados
            self.num_vertices += 1
            return True
        return False

    def adicionar_aresta(self, u, v, peso=1, direcionado=False):

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

        return self.num_vertices

    def obter_numero_arestas(self):

        return self.num_arestas

    def obter_vertices(self):

        return list(self.lista_adj.keys())

    def obter_vizinhos(self, vertice):

        return self.lista_adj.get(vertice, {})

    def __str__(self):

        if self.num_vertices == 0:
            return "Grafo Vazio"
        
        output = f"Grafo com {self.num_vertices} vértices e {self.num_arestas} arestas.\n"
        output += "Lista de Adjacências (Vértice -> {Vizinho: Peso}):\n"
        for vertice, vizinhos in self.lista_adj.items():
            output += f"  {vertice}: {vizinhos}\n"
        return output