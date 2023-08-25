import os
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.patches as mpatches

def calcular_centralidade(grafo):
    """Calcula a centralidade dos nós do grafo."""
    return nx.betweenness_centrality(grafo, weight='weight')

def salvar_centralidade(centralidade, grafo, ano):
    """Salva a lista ordenada de centralidade em um arquivo .png."""
    sorted_centralidade = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)
    
    # Modificar os rótulos para incluir o partido antes do nome do deputado
    rótulos = [f"({grafo.nodes[no]['partido']}) {no}" for no in [item[0] for item in sorted_centralidade]]
    
    fig, ax = plt.subplots(figsize=(10, 15))
    valores = [item[1] for item in sorted_centralidade]
    
    ax.barh(rótulos, valores, color='blue')
    ax.invert_yaxis()  # Inverter o eixo y para exibir os maiores valores no topo
    ax.set_xlabel('Centralidade')
    ax.set_ylabel('Deputados')
    ax.set_title(f'Centralidade dos Deputados - {ano}')
    plt.tight_layout()
    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/centralidade_{ano}.png")
    plt.close()

def salvar_heatmap(grafo, ano):
    """Salva um heatmap da matriz de adjacência em um arquivo .png, incluindo o partido nos rótulos."""
    matriz_adjacencia = nx.to_pandas_adjacency(grafo, weight='weight')
    
    # Modificar os rótulos do índice e das colunas para incluir o partido
    rotulos = [f"{no} ({grafo.nodes[no]['partido']})" for no in matriz_adjacencia.index]
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
    
    # Utilizando um layout tipo spring para melhor visualização
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
    
    # Desenhando os nós com cores baseadas no atributo partido
    cores_nos = [cores_partidos[grafo.nodes[no]['partido']] for no in grafo.nodes]
    
    # Desenhar os nós e arestas
    nx.draw_networkx_nodes(grafo, pos=posicao, node_size=500, node_color=cores_nos, alpha=0.8)
    nx.draw_networkx_labels(grafo, pos=posicao, font_size=10, verticalalignment='bottom')
    nx.draw_networkx_edges(grafo, pos=posicao, alpha=0.5)

    # Identificar os partidos presentes no grafo
    partidos_presentes = set(nx.get_node_attributes(grafo, 'partido').values())

    # Criar uma legenda somente para os partidos presentes
    legend_handles = [mpatches.Patch(color=cores_partidos[partido], label=partido) 
                      for partido in partidos_presentes]
    
    plt.legend(handles=legend_handles, loc="upper left", title="Partidos")
    
    plt.title(f"Grafo de Votação dos Deputados - {ano}")
    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/grafo_{ano}")
    plt.close()
    