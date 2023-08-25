
import os
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def calcular_centralidade(grafo):
    """Calcula a centralidade dos nós do grafo."""
    return nx.betweenness_centrality(grafo, weight='weight')

def salvar_centralidade(centralidade, ano):
    """Salva a lista ordenada de centralidade em um arquivo .png."""
    sorted_centralidade = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)
    
    fig, ax = plt.subplots(figsize=(10, 15))
    deputados = [item[0] for item in sorted_centralidade]
    valores = [item[1] for item in sorted_centralidade]
    
    ax.barh(deputados, valores, color='blue')
    ax.invert_yaxis()  # Inverte o exito y para mostrar os maiores valores no topo
    ax.set_xlabel('Centralidade')
    ax.set_title(f'Centralidade dos Deputados - {ano}')
    plt.tight_layout()
    
    # Verifica se o diretório "images" existe, caso não, ele é criado
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/centralidade_{ano}.png")
    plt.close()

def salvar_heatmap(grafo, ano):
    """Salva um heatmap da matriz de adjacência em um arquivo .png."""
    matriz_adjacencia = nx.to_pandas_adjacency(grafo, weight='weight')
    
    plt.figure(figsize=(15, 15))
    sns.heatmap(matriz_adjacencia, cmap='coolwarm', center=0)
    plt.title(f"Heatmap de Correlação entre Deputados - {ano}")

    # Verifica se o diretório "images" existe, caso não, ele é criado
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/heatmap_{ano}.png")
    plt.close()

def salvar_grafo(grafo, ano):
    """Salva a visualização do grafo em um arquivo .png."""
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(grafo)
    nx.draw_networkx_nodes(grafo, pos, node_size=10, node_color="blue")
    nx.draw_networkx_edges(grafo, pos, alpha=0.1)
    plt.title(f"Grafo de Votações - {ano}")

    # Verifica se o diretório "images" existe, caso não, ele é criado
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/grafo_{ano}.png")
    plt.close()
