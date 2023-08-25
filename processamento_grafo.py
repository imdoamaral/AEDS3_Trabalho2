
import networkx as nx
import pandas as pd

class GrafoVotacoes:
    def __init__(self):
        self.grafo = nx.Graph()

    def carregar_dados(self, ano):
        """Carrega os dados dos políticos e do grafo dos arquivos CSV correspondentes ao ano fornecido."""
        dados_politicos = pd.read_csv(f"datasets/politicians{ano}.csv", encoding='utf-8', delimiter=';', header=None, names=['deputado', 'partido', 'votos'], engine='python')
        dados_grafo = pd.read_csv(f"datasets/graph{ano}.csv", encoding='utf-8', delimiter=';', header=None, names=['deputado1', 'deputado2', 'peso'], engine='python')
        return dados_politicos, dados_grafo

    def criar_grafo(self, dados_politicos, dados_grafo):
        """Cria o grafo a partir dos dados fornecidos."""
        # Adiciona os nós (deputados) ao grafo
        for _, linha in dados_politicos.iterrows():
            self.grafo.add_node(linha['deputado'], partido=linha['partido'], votos=linha['votos'])

        # Adiciona as arestas (relações de votos em comum) ao grafo
        for _, linha in dados_grafo.iterrows():
            self.grafo.add_edge(linha['deputado1'], linha['deputado2'], weight=linha['peso'])

    def filtrar_por_partido(self, partidos):
        """Filtra o grafo com base na lista de partidos fornecida."""
        nos_a_remover = [no for no, attr in self.grafo.nodes(data=True) if attr['partido'] not in partidos]
        self.grafo.remove_nodes_from(nos_a_remover)
        
    def normalizar_pesos(self):
        """Normaliza o peso das arestas no intervalo [0, 1]."""
        for u, v, data in self.grafo.edges(data=True):
            data['weight'] = data['weight'] / min(self.grafo.nodes[u]['votos'], self.grafo.nodes[v]['votos'])

    def aplicar_threshold(self, threshold):
        """Aplica um limiar no grafo, removendo arestas com peso inferior ao threshold."""
        arestas_a_remover = [(u, v) for u, v, data in self.grafo.edges(data=True) if data['weight'] < threshold]
        self.grafo.remove_edges_from(arestas_a_remover)

    def inverter_pesos(self):
        """Inverte os pesos das arestas conforme a formula: w(u, v) = 1/w(u, v)."""
        for u, v, data in self.grafo.edges(data=True):
            data['weight'] = 1 / data['weight']

