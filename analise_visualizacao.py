import os
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.patches as mpatches

def calcular_centralidade(grafo):
    """Calcula a centralidade dos nós do grafo."""
    return nx.betweenness_centrality(grafo, weight='weight')

def salvar_centralidade(centralidade, grafo, ano, N=80):
    """Salva a lista ordenada de centralidade em um arquivo .png com os N deputados de maior centralidade."""
    sorted_centralidade = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)[:N]
    
    # Modifica os rótulos para incluir o partido após o nome do deputado
    rotulos = [f"{no} ({grafo.nodes[no]['partido']})" for no in [item[0] for item in sorted_centralidade]]
    
    fig, ax = plt.subplots(figsize=(15, 15))
    valores = [item[1] for item in sorted_centralidade]
    
    ax.barh(rotulos, valores, color='blue')
    ax.invert_yaxis()  # Inverte o eixo y para mostrar os maiores valores no topo
    ax.set_xlabel('Centralidade')
    ax.set_ylabel('Deputados')
    ax.set_title(f'Centralidade dos Deputados - {ano}')
    plt.tight_layout(pad=2)  # Aumenta o padding
    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/centralidade_{ano}.png")
    plt.close()

def salvar_heatmap(grafo, ano):
    """Salva um heatmap da matriz de adjacência em um arquivo .png, incluindo o partido nos rótulos."""
    
    # Cria uma lista ordenada de nós com base no atributo do partido
    nos_ordenados = sorted(grafo.nodes(data=True), key=lambda x: x[1]['partido'])
    
    # Reordena o grafo com base na lista ordenada de nós
    grafo_ordenado = nx.Graph()
    grafo_ordenado.add_nodes_from([(no[0], no[1]) for no in nos_ordenados])
    grafo_ordenado.add_weighted_edges_from([(u, v, grafo[u][v]['weight']) for u, v in grafo.edges()])
    
    # Cria a matriz de adjacência a partir do grafo reordenado
    matriz_adjacencia = nx.to_pandas_adjacency(grafo_ordenado, weight='weight')
    
    # Modifica os rótulos do índice e das colunas para incluir o partido
    rotulos = [f"{no} ({grafo_ordenado.nodes[no]['partido']})" for no in matriz_adjacencia.index]
    matriz_adjacencia.index = rotulos
    matriz_adjacencia.columns = rotulos
    
    plt.figure(figsize=(20, 20))
    sns.heatmap(matriz_adjacencia, cmap='coolwarm', center=0)
    plt.title(f"Heatmap de Correlação entre Deputados - {ano}")

    # Verifica se o diretório "images" existe, caso não, ele é criado
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/heatmap_{ano}.png")
    plt.close()

def salvar_grafo(grafo, ano):
    plt.figure(figsize=(15, 15))
    
    # Utiliza um layout do tipo spring para melhor visualização
    posicao = nx.spring_layout(grafo, k=0.3)

    cores_partidos = {
        'PT': 'red',
        'PSOL': 'yellow',
        'MDB': 'green',
        'PSDB': 'lightblue',
        'DEM': 'blue',
        'PDT': 'darkgreen',
        'PL': 'mediumblue'
    }
    
    # Desenha os nós com cores baseadas no partido
    cores_nos = [cores_partidos[grafo.nodes[no]['partido']] for no in grafo.nodes]
    
    # Desenha os nós e arestas
    nx.draw_networkx_nodes(grafo, pos=posicao, node_size=500, node_color=cores_nos, alpha=0.8)
    nx.draw_networkx_labels(grafo, pos=posicao, font_size=10, verticalalignment='bottom')
    nx.draw_networkx_edges(grafo, pos=posicao, alpha=0.5)

    # Identifica os partidos presentes no grafo
    partidos_presentes = set(nx.get_node_attributes(grafo, 'partido').values())

    # Cria uma legenda somente para os partidos presentes
    legend_handles = [mpatches.Patch(color=cores_partidos[partido], label=partido) 
                      for partido in partidos_presentes]
    
    plt.legend(handles=legend_handles, loc="upper left", title="Partidos")
    
    plt.title(f"Grafo de Votação dos Deputados - {ano}")
    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/grafo_{ano}")
    plt.close()
    