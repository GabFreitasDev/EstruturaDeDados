import networkx as nx
import matplotlib.pyplot as plt

class Graph:

    def __init__(self, graph):
        self.graph = graph  # grafo residual
        self.ROW = len(graph)
        # self.COL = len(gr[0])

    '''Retorna verdadeiro se houver um caminho da fonte 's' para o sumidouro 't' no
    grafo residual. Também preenche parent[] para armazenar o caminho'''

    def BFS(self, s, t, parent):

        # Marca todos os vértices como não visitados
        visited = [False]*(self.ROW)

        # Cria uma fila para BFS
        queue = []

        # Marca o nó de origem como visitado e o coloca na fila
        queue.append(s)
        visited[s] = True

        # Loop padrão do BFS
        while queue:

            # Remove um vértice da fila
            u = queue.pop(0)

            # Obtém todos os vértices adjacentes do vértice removido u
            # Se um adjacente não foi visitado, então marca como
            # visitado e coloca na fila
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    # Se encontrarmos uma conexão para o nó sumidouro,
                    # então não há mais sentido em continuar o BFS
                    # Basta definir seu pai e retornar verdadeiro
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True

        # Não alcançamos o sumidouro no BFS iniciado
        # a partir da fonte, então retorna falso
        return False
        

    # Retorna o fluxo máximo de s para t no grafo dado
    def fordFulkerson(self, source, sink):

        # Este array é preenchido pelo BFS para armazenar o caminho
        parent = [-1]*(self.ROW)

        max_flow = 0 # Inicialmente não há fluxo

        # Aumenta o fluxo enquanto houver caminho da fonte para o sumidouro
        while self.BFS(source, sink, parent):

            # Encontra a capacidade residual mínima das arestas ao longo do
            # caminho encontrado pelo BFS. Ou podemos dizer que encontra o fluxo máximo
            # através do caminho encontrado.
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Adiciona o fluxo do caminho ao fluxo total
            max_flow += path_flow

            # atualiza as capacidades residuais das arestas e arestas reversas
            # ao longo do caminho
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

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

graph = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]

mostraGrafo(graph)
g = Graph(graph)

source = 0; sink = 5
 
print ("O Fluxo maximo e igual a %d " % g.f(source, sink))
