import networkx as nx
import matplotlib.pyplot as plt

class Grafo:

    def __init__(self, grafo):
        self.grafo = grafo  # grafo residual
        self.ROW = len(grafo)

    def BFS(self, fonte, target, parent):

        # Marca todos os vértices como não visitados
        visited = [False]*(self.ROW)
        fila = []

        fila.append(fonte)
        visited[fonte] = True

        # Loop padrão do BFS
        while fila:

            vertice = fila.pop(0)

            # Obtém todos os vértices próximos do vértice removido
            # se um próximo não foi visitado, então marca como
            # visitado e coloca na fila
            for i, val in enumerate(self.grafo[vertice]):
                if visited[i] == False and val > 0:
                    # Se encontrarmos uma conexão para o último então não precisa mais continuar o BFS
                    fila.append(i)
                    visited[i] = True
                    parent[i] = vertice
                    if i == target:
                        return True

        return False
        
    def fordFulkerson(self, fonte, target):

        # Este array é preenchido pelo BFS para armazenar o caminho
        parent = [-1]*(self.ROW)

        fluxoMax = 0 # Inicialmente não há fluxo

        # Aumenta o fluxo enquanto houver caminho da fonte para o último nó
        while self.BFS(fonte, target, parent):
            caminhoFluxo = float("Inf")
            tempObj = target

            # Calcula fluxo e atualiza capacidades
            while(tempObj != fonte):
                caminhoFluxo = min(caminhoFluxo, self.grafo[parent[tempObj]][tempObj])
                tempObj = parent[tempObj]

            fluxoMax += caminhoFluxo

            # Reinicia o percurso para atualizar as capacidades
            tempObj = target
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

fonte = 0; target = 5
 
print ("O Fluxo maximo e igual a %d " % g.f(fonte, target))
