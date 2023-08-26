import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def criar_pasta_resultados():
    """
    Cria a pasta 'resultados' se ela não existir.
    """
    if not os.path.exists('resultados'):
        os.makedirs('resultados')

def gerar_grafo(df):
    """
    Gera um grafo com base nos dados fornecidos.
    
    Args:
    - df (DataFrame): Dados do grafo.
    
    Retorna:
    - Graph: Grafo gerado.
    """
    G = nx.from_pandas_edgelist(df, 'DeputadoA', 'DeputadoB', ['PesoNormalizado'])
    return G

def plotar_centralidade(G, ano, partidos, threshold, df_politicos):
    centralidades = nx.betweenness_centrality(G, weight='PesoNormalizado', normalized=True)
    centralidades_ordenadas = sorted(centralidades.items(), key=lambda x: x[1], reverse=True)

    # Extrair valores para plotagem
    nomes, valores = zip(*centralidades_ordenadas)

    # Criar a representação "(Partido) Nome" usando o df_politicos
    nome_partido_map = df_politicos.set_index('Nome').apply(lambda row: f"({row['Partido']}) {row.name}", axis=1).to_dict()
    nomes = [nome_partido_map.get(nome, nome) for nome in nomes]

    plt.figure(figsize=(20, 12))
    sns.barplot(x=list(nomes)[:20], y=list(valores)[:20], palette='viridis')
    plt.title(f'Centralidade de Betweenness - {ano}')
    plt.ylabel('Centralidade')
    plt.xlabel('Deputado')
    plt.xticks(rotation=45)
    # Ajusta o layout para não cortar nenhum texto
    plt.tight_layout()

    # Salvar figura
    nome_partidos = "-".join(partidos) if partidos else "TODOS"
    plt.savefig(f'resultados/betweness_{ano}_{nome_partidos}_threshold{threshold}.png')
    plt.show()



def plotar_heatmap(df, ano, partidos, threshold, df_politicos):
    # Criar a representação "(Partido) Nome" usando o df_politicos
    nome_partido_map = df_politicos.set_index('Nome').apply(lambda row: f"({row['Partido']}) {row.name}", axis=1).to_dict()
    df['DeputadoA'] = df['DeputadoA'].map(nome_partido_map)
    df['DeputadoB'] = df['DeputadoB'].map(nome_partido_map)

    # Pivot para obter matriz de correlação
    matrix = df.pivot(index='DeputadoA', columns='DeputadoB', values='PesoNormalizado')
    matrix.fillna(0, inplace=True)

    # Calcular correlação
    correlacao = matrix.corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlacao, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title(f'Heatmap de Correlação - {ano}')

    # Ajusta o layout para não cortar nenhum texto
    plt.tight_layout()

    # Salvar figura
    nome_partidos = "-".join(partidos) if partidos else "TODOS"
    plt.savefig(f'resultados/heatmap_{ano}_{nome_partidos}_threshold{threshold}.png')
    plt.show()



def plotar_grafo(G, ano, partidos, df_politicos, threshold):
    """
    Plota o grafo das conexões.
    
    Args:
    - G (Graph): Grafo.
    - ano (int): Ano de referência.
    - partidos (list): Lista de partidos considerados.
    - df_politicos (DataFrame): Dados dos políticos.
    """
    plt.figure(figsize=(12, 12))

    # Associar cada deputado ao seu partido
    partido_map = df_politicos.set_index('Nome')['Partido'].to_dict()
    cores_partidos = sns.color_palette('husl', len(partidos))
    cor_map = dict(zip(partidos, cores_partidos))
    node_colors = [cor_map.get(partido_map[node], '#333333') for node in G.nodes()]

    pos = nx.spring_layout(G)
    
    # Desenhar arestas com opacidade reduzida
    nx.draw_networkx_edges(G, pos, edge_color="#e1e1e1", width=[G[u][v]['PesoNormalizado'] for u, v in G.edges()])
    
    # Desenhar nós e rótulos
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=200)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    plt.title(f'Grafo das Conexões - {ano}')

    # Criar legenda
    legenda = [plt.Line2D([0], [0], color=cor, marker='o', markersize=10, label=partido) for partido, cor in cor_map.items()]
    plt.legend(handles=legenda, loc='upper left')

    # Ajusta o layout para não cortar nenhum texto
    plt.tight_layout()
    
    # Salvar figura
    nome_partidos = "-".join(partidos) if partidos else "TODOS"
    plt.savefig(f'resultados/graph_{ano}_{nome_partidos}_threshold{threshold}.png')
    plt.show()