import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class FootballNetworkAnalysis:
    def __init__(self):
        # Configurar os times e grafos
        self.setup_teams()
        self.setup_passes()
        
        # Definir jogadores padrão 
        self.fonte_br = 'Alisson'
        self.coletor_br = 'Neymar'
        self.fonte_ar = 'Dibu Martínez'
        self.coletor_ar = 'Messi'
    
    def setup_teams(self):
        """Configura as equipes do Brasil e Argentina"""
        # Configuração 4-3-3 do Brasil
        self.brasil = {
            'Goleiro': {'Alisson': 1},
            'Laterais': {'Danilo': 2, 'Alex Sandro': 6},
            'Zagueiros': {'Marquinhos': 4, 'Thiago Silva': 3},
            'Meio-campo': {'Casemiro': 5, 'Fabinho': 8, 'Bruno Guimarães': 17},
            'Atacantes': {'Neymar': 10, 'Vini Jr': 20, 'Raphinha': 19}
        }

        # Configuração 4-3-3 da Argentina
        self.argentina = {
            'Goleiro': {'Dibu Martínez': 23},
            'Laterais': {'Molina': 26, 'Tagliafico': 3},
            'Zagueiros': {'Otamendi': 19, 'Romero': 13},
            'Meio-campo': {'De Paul': 7, 'Enzo': 24, 'Mac Allister': 20},
            'Atacantes': {'Messi': 10, 'Di María': 11, 'Julián Álvarez': 9}
        }

        # Criando os grafos
        self.G_br = nx.DiGraph()
        self.G_ar = nx.DiGraph()

        # Adicionando nós com atributos
        for time, G in [(self.brasil, self.G_br), (self.argentina, self.G_ar)]:
            for posicao, players in time.items():
                for nome, numero in players.items():
                    G.add_node(nome, posicao=posicao, numero=numero, 
                              passes_feitos=0, passes_recebidos=0, 
                              time='Brasil' if G == self.G_br else 'Argentina')
    
    def setup_passes(self):
        """Configura os passes para ambos os times"""
        # Passes no Brasil
        passes_br = [
            # Goleiro (Alisson)
            ('Alisson', 'Marquinhos', 10), ('Alisson', 'Casemiro', 5),
        
            # Laterais
            ('Danilo', 'Casemiro', 18), ('Danilo', 'Neymar', 8),
            ('Alex Sandro', 'Fabinho', 16), ('Alex Sandro', 'Raphinha', 4),
        
            # Zagueiros
            ('Marquinhos', 'Casemiro', 22), ('Marquinhos', 'Neymar', 8),
            ('Thiago Silva', 'Fabinho', 20), ('Thiago Silva', 'Casemiro', 18),
        
            # Meio-campo
            ('Casemiro', 'Neymar', 18), ('Casemiro', 'Bruno Guimarães', 25),
            ('Fabinho', 'Bruno Guimarães', 22), ('Fabinho', 'Vini Jr', 12),
            ('Bruno Guimarães', 'Neymar', 20), ('Bruno Guimarães', 'Vini Jr', 12),
        
            # Atacantes
            ('Neymar', 'Vini Jr', 25), ('Neymar', 'Raphinha', 20),
            ('Vini Jr', 'Neymar', 15), ('Vini Jr', 'Raphinha', 12),
            ('Raphinha', 'Neymar', 18), ('Raphinha', 'Vini Jr', 14)
        ]

        # Passes na Argentina
        passes_ar = [
            # Goleiro (Dibu Martínez)
            ('Dibu Martínez', 'Otamendi', 9), ('Dibu Martínez', 'De Paul', 5),
        
            # Laterais
            ('Molina', 'De Paul', 18), ('Molina', 'Messi', 8),
            ('Tagliafico', 'Mac Allister', 14), ('Tagliafico', 'Di María', 10),
        
            # Zagueiros
            ('Otamendi', 'De Paul', 20), ('Otamendi', 'Messi', 8),
            ('Romero', 'Mac Allister', 18), ('Romero', 'De Paul', 16),
        
            # Meio-campo
            ('De Paul', 'Messi', 20), ('De Paul', 'Enzo', 22),
            ('Mac Allister', 'Enzo', 18), ('Mac Allister', 'Di María', 16),
            ('Enzo', 'Messi', 25), ('Enzo', 'Di María', 10),
        
            # Atacantes
            ('Messi', 'Di María', 30), ('Messi', 'Julián Álvarez', 20),
            ('Di María', 'Messi', 28), ('Di María', 'Julián Álvarez', 15),
            ('Julián Álvarez', 'Messi', 22), ('Julián Álvarez', 'Di María', 18)
        ]

        # Adicionando os passes
        self.adicionar_passes(self.G_br, passes_br)
        self.adicionar_passes(self.G_ar, passes_ar)
    
    def adicionar_passes(self, G, passes):
        """Adiciona passes ao grafo"""
        for origem, destino, qtd in passes:
            G.add_edge(origem, destino, weight=qtd)
            G.nodes[origem]['passes_feitos'] += qtd
            G.nodes[destino]['passes_recebidos'] += qtd
    
    def ford_fulkerson_bfs(self, G, source, sink):
        """Implementação do algoritmo Ford-Fulkerson com BFS"""
        # Criar grafo residual
        residual = nx.DiGraph()
        for u, v, data in G.edges(data=True):
            residual.add_edge(u, v, capacity=data['weight'])
            residual.add_edge(v, u, capacity=0)  # Aresta reversa
        
        # Função BFS para encontrar caminhos aumentativos
        def bfs():
            visited = {node: False for node in residual.nodes()}
            parent = {}
            queue = deque([source])
            visited[source] = True
            
            while queue:
                u = queue.popleft()
                for v in residual.neighbors(u):
                    if not visited[v] and residual[u][v]['capacity'] > 0:
                        visited[v] = True
                        parent[v] = u
                        queue.append(v)
                        if v == sink:
                            return parent
            return None
        
        # Aumentar fluxo enquanto houver caminhos
        max_flow = 0
        parent = bfs()
        while parent:
            path_flow = float('inf')
            v = sink
            
            # Calcular fluxo mínimo no caminho
            path_edges = []
            while v != source:
                u = parent[v]
                path_edges.append((u, v))
                path_flow = min(path_flow, residual[u][v]['capacity'])
                v = u
            
            # Atualizar capacidades residuais
            for u, v in path_edges:
                residual[u][v]['capacity'] -= path_flow
                residual[v][u]['capacity'] += path_flow
            
            max_flow += path_flow
            parent = bfs()
        
        return max_flow
    
    def visualizar_grafo(self):
        """Visualiza o grafo com os fluxos calculados"""
        # Calcular fluxo máximo
        fluxo_br = self.ford_fulkerson_bfs(self.G_br, self.fonte_br, self.coletor_br)
        fluxo_ar = self.ford_fulkerson_bfs(self.G_ar, self.fonte_ar, self.coletor_ar)
        
        # Configurar figura
        plt.figure(figsize=(20, 14))
        
        # Posicionamento em campo
        pos_br = {
            'Alisson': (2, 0),
            'Danilo': (4, -3), 'Marquinhos': (4, -1), 
            'Thiago Silva': (4, 1), 'Alex Sandro': (4, 3),
            'Casemiro': (6, -1), 'Fabinho': (6, 0), 'Bruno Guimarães': (6, 1),
            'Raphinha': (8, -2), 'Neymar': (8, 0), 'Vini Jr': (8, 2)
        }
        
        pos_ar = {
            'Dibu Martínez': (18, 0),
            'Molina': (16, -3), 'Otamendi': (16, -1),
            'Romero': (16, 1), 'Tagliafico': (16, 3),
            'De Paul': (14, -1), 'Enzo': (14, 0), 'Mac Allister': (14, 1),
            'Di María': (12, -2), 'Messi': (12, 0), 'Julián Álvarez': (12, 2)
        }
        
        # Desenhar campo de futebol
        self.desenhar_campo()
        
        # Cores dos times
        cores = {'Brasil': '#FFDF00', 'Argentina': '#6CACE4'}
        
        # Desenhar nós com destaque para fonte e coletor
        for G, pos, time in [(self.G_br, pos_br, 'Brasil'), (self.G_ar, pos_ar, 'Argentina')]:
            node_colors = []
            for node in G.nodes():
                if node == (self.fonte_br if time == 'Brasil' else self.fonte_ar):
                    node_colors.append('green')  # Fonte em verde
                elif node == (self.coletor_br if time == 'Brasil' else self.coletor_ar):
                    node_colors.append('red')    # Coletor em vermelho
                else:
                    node_colors.append(cores[time])
            
            nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=node_colors, edgecolors='black')
        
        # Rótulos com informações
        labels_br = {n: f"{n.split()[0]}\n#{self.G_br.nodes[n]['numero']}\n▲{self.G_br.nodes[n]['passes_feitos']}▼{self.G_br.nodes[n]['passes_recebidos']}" 
                    for n in self.G_br.nodes()}
        labels_ar = {n: f"{n.split()[0]}\n#{self.G_ar.nodes[n]['numero']}\n▲{self.G_ar.nodes[n]['passes_feitos']}▼{self.G_ar.nodes[n]['passes_recebidos']}" 
                    for n in self.G_ar.nodes()}
        
        nx.draw_networkx_labels(self.G_br, pos_br, labels=labels_br, font_size=7, font_weight='bold')
        nx.draw_networkx_labels(self.G_ar, pos_ar, labels=labels_ar, font_size=7, font_weight='bold')
        
        # Desenhar arestas
        edge_width_br = [d['weight']*0.03 for u,v,d in self.G_br.edges(data=True)]
        nx.draw_networkx_edges(self.G_br, pos_br, width=edge_width_br, arrowstyle='-|>', 
                              arrowsize=12, edge_color='#333333', node_size=1000, alpha=0.7)
        
        edge_width_ar = [d['weight']*0.03 for u,v,d in self.G_ar.edges(data=True)]
        nx.draw_networkx_edges(self.G_ar, pos_ar, width=edge_width_ar, arrowstyle='-|>', 
                              arrowsize=12, edge_color='#333333', node_size=1000, alpha=0.7)
        
        # Adicionar informações de fluxo e legenda
        self.adicionar_informacoes(fluxo_br, fluxo_ar)
        
        plt.title("Análise de Fluxo de Passes - Ford-Fulkerson", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.xlim(-1, 21)
        plt.ylim(-9, 5)
        plt.tight_layout()
        plt.show()
    
    def desenhar_campo(self):
        """Desenha o campo de futebol como fundo"""
        plt.plot([0,20], [0,0], 'g-', linewidth=1, alpha=0.5)
        plt.plot([10,10], [-5,5], 'w-', linewidth=2)
        plt.plot([0,0], [-5,5], 'g-', linewidth=2)
        plt.plot([20,20], [-5,5], 'g-', linewidth=2)
    
    def adicionar_informacoes(self, fluxo_br, fluxo_ar):
        """Adiciona informações textuais ao gráfico"""
        plt.text(1, -8, f"Fluxo Brasil: {fluxo_br} (de {self.fonte_br} para {self.coletor_br})", 
                fontsize=12, color='#FFDF00', weight='bold')
        plt.text(15, -8, f"Fluxo Argentina: {fluxo_ar} (de {self.fonte_ar} para {self.coletor_ar})", 
                fontsize=12, color='#6CACE4', weight='bold')
        
        plt.text(1, -6, "Legenda:", fontweight='bold')
        plt.text(1, -6.5, "▲ Passes realizados", fontsize=8)
        plt.text(1, -7, "▼ Passes recebidos", fontsize=8)
        plt.text(1, -7.5, "Amarelo: Brasil | Azul: Argentina", fontsize=8)
        plt.text(1, -8.5, "Verde: Fonte | Vermelho: Coletor", fontsize=8)
        
        plt.text(10, -8.5, "Algoritmo Ford-Fulkerson para calcular fluxo máximo de passes", 
                fontsize=10, ha='center', weight='bold')

# Executar a análise
if __name__ == "__main__":
    analise = FootballNetworkAnalysis()
    
    # Visualizar o grafo com os fluxos
    analise.visualizar_grafo()