import networkx as nx
import matplotlib.pyplot as plt

class Grafo:

    def __init__(self, grafo):
        self.grafo = grafo  # grafo residual
        self.ROW = len(grafo)

    def DFS(self, s, t, parent, visited):
        visited[s] = True

        if s == t:
            return True

        for ind, val in enumerate(self.grafo[s]):
            if not visited[ind] and val > 0:
                parent[ind] = s
                if self.DFS(ind, t, parent, visited):
                    return True
        return False
        
    def fordFulkerson(self, fonte, coletor):
        parent = [-1]*(self.ROW)
        fluxoMax = 0 

        # Aumenta o fluxo enquanto houver caminho da fonte para o último nó
        while True:
            visited = [False] * self.ROW
            if not self.DFS(fonte, coletor, parent, visited):
                break

            caminhoFluxo = float("Inf")
            tempObj = coletor

            # Calcula fluxo e atualiza capacidades
            while(tempObj != fonte):
                caminhoFluxo = min(caminhoFluxo, self.grafo[parent[tempObj]][tempObj])
                tempObj = parent[tempObj]

            fluxoMax += caminhoFluxo

            # Reinicia o percurso para atualizar as capacidades
            tempObj = coletor
            while(tempObj != fonte):
                vertice = parent[tempObj]
                self.grafo[vertice][tempObj] -= caminhoFluxo
                self.grafo[tempObj][vertice] += caminhoFluxo
                tempObj = parent[tempObj]

        return fluxoMax

def mostraGrafo(graph_matrix):
    G = nx.DiGraph()
    
    for i in range(len(graph_matrix)):
        for j in range(len(graph_matrix[i])):
            if graph_matrix[i][j] > 0:
                G.add_edge(i, j, capacity=graph_matrix[i][j])
    
    pos = nx.spring_layout(G)
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
