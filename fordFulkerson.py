import networkx as nx
import matplotlib.pyplot as plt

class Grafo:

    def __init__(self, grafo):
        self.grafo = grafo
        self.ROW = len(grafo) # Número de vértices

    def DFS(self, fonte, coletor, parent, visited):
        # Encontra caminhos aumentantes recursivamente
        # Usa 'visited' para evitar ciclos e 'parent' para reconstruir caminhos
        visited[fonte] = True

        if fonte == coletor:
            return True

        for i, val in enumerate(self.grafo[fonte]):
            if not visited[i] and val > 0:
                parent[i] = fonte
                if self.DFS(i, coletor, parent, visited):
                    return True
        return False
        
    def fordFulkerson(self, fonte, coletor):
        parent = [-1]*(self.ROW)
        fluxoMax = 0 

        # Aumenta o fluxo enquanto houver caminho da fonte para o último nó
        while True:
            visited = [False] * self.ROW
            if not self.DFS(fonte, coletor, parent, visited):
                break # Para quando não há mais caminhos

            caminhoFluxo = float("Inf")
            tempObj = coletor

            # Calcula fluxo e atualiza capacidades
            while(tempObj != fonte):
                vertice = parent[tempObj]
                caminhoFluxo = min(caminhoFluxo, self.grafo[vertice][tempObj])
                tempObj = vertice

            fluxoMax += caminhoFluxo

            # Reinicia o percurso para atualizar as capacidades
            tempObj = coletor
            while(tempObj != fonte):
                vertice = parent[tempObj]
                self.grafo[vertice][tempObj] -= caminhoFluxo
                self.grafo[tempObj][vertice] += caminhoFluxo # Aresta reversa
                tempObj = parent[tempObj]

        return fluxoMax

def mostraGrafo(graph_matrix):
    G = nx.DiGraph()
    
    for i in range(len(graph_matrix)):
        for j in range(len(graph_matrix[i])):
            if graph_matrix[i][j] > 0:
                G.add_edge(i, j, capacity=graph_matrix[i][j])
    
    pos = nx.spring_layout(G)
    # Usa NetworkX para desenhar o grafo
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

# Cria um grafo conforme o diagrama abaixo

grafo = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]

mostraGrafo(grafo)
g = Grafo(grafo)
fonte = 0; coletor = 5
fluxoMax = g.fordFulkerson(fonte, coletor)
 
print("Fluxo Máximo: ", fluxoMax)
