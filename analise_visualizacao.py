import os
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.patches as mpatches

def calcular_centralidade(grafo):
    """Calcula a centralidade dos nós do grafo."""
    return nx.betweenness_centrality(grafo, weight='weight')

def salvar_centralidade(centralidade, grafo, ano, N=100):
    """Salva a lista ordenada de centralidade em um arquivo .png com os N deputados de maior centralidade."""
    sorted_centralidade = sorted(centralidade.items(), key=lambda x: x[1], reverse=True)[:N]
    
    # Modificar os rótulos para incluir o partido após o nome do deputado
    rotulos = [f"{no} ({grafo.nodes[no]['partido']})" for no in [item[0] for item in sorted_centralidade]]
    
    fig, ax = plt.subplots(figsize=(15, 15))
    valores = [item[1] for item in sorted_centralidade]
    
    ax.barh(rotulos, valores, color='blue')
    ax.invert_yaxis()  # Invert y axis to display the highest values at the top
    ax.set_xlabel('Centralidade')
    ax.set_ylabel('Deputados')
    ax.set_title(f'Centralidade dos Deputados - {ano}')
    plt.tight_layout(pad=2)  # Aumentar o padding
    
    if not os.path.exists("images"):
        os.makedirs("images")
    
    plt.savefig(f"images/centralidade_{ano}.png")
    plt.close()

def salvar_heatmap(grafo, ano):
    """Salva um heatmap da matriz de adjacência em um arquivo .png, com deputados agrupados por partido."""
    
    # Convertendo o grafo para uma matriz de adjacência no formato DataFrame
    matriz_adjacencia = nx.to_pandas_adjacency(grafo, weight='weight')
    
    # Criando uma lista ordenada dos partidos com base na quantidade de deputados
    contagem_partidos = {}
    for node, data in grafo.nodes(data=True):
        partido = data['partido']
        contagem_partidos[partido] = contagem_partidos.get(partido, 0) + 1
    partidos_ordenados = sorted(contagem_partidos.keys(), key=lambda x: -contagem_partidos[x])
    
    # Ordenando os deputados na matriz de adjacência com base nos partidos
    deputados_ordenados = sorted(matriz_adjacencia.index, key=lambda x: (partidos_ordenados.index(grafo.nodes[x]['partido']), x))
    matriz_adjacencia = matriz_adjacencia.reindex(deputados_ordenados)
    matriz_adjacencia = matriz_adjacencia[deputados_ordenados]
    
    # Modificar os rótulos do índice e das colunas para incluir o partido
    rotulos = [f"{no} ({grafo.nodes[no]['partido']})" for no in matriz_adjacencia.index]
    matriz_adjacencia.index = rotulos
    matriz_adjacencia.columns = rotulos

    plt.figure(figsize=(20, 20))
    
    # Desenhando o heatmap
    sns.heatmap(matriz_adjacencia, cmap='coolwarm', center=0)

    # Adicionando o título
    plt.title(f"Heatmap de Correlação entre Deputados - {ano}")

    # Verificando se o diretório "images" existe e salvando a figura
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
    