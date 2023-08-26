import pandas as pd
import numpy as np

def ler_politicos(ano):
    """
    Lê o arquivo de políticos para o ano especificado.
    
    Args:
    - ano (int): Ano de referência para leitura do arquivo.
    
    Retorna:
    - DataFrame: Dados dos políticos para o ano especificado.
    """
    return pd.read_csv(f'datasets/politicians{ano}.csv', sep=';', names=['Nome', 'Partido', 'Votacoes'])

def ler_grafo(ano):
    """
    Lê o arquivo de grafo para o ano especificado.
    
    Args:
    - ano (int): Ano de referência para leitura do arquivo.
    
    Retorna:
    - DataFrame: Dados do grafo para o ano especificado.
    """
    return pd.read_csv(f'datasets/graph{ano}.csv', sep=';', names=['DeputadoA', 'DeputadoB', 'Concordancias'])

def filtrar_partidos(df, partidos):
    """
    Filtra os dados do DataFrame com base nos partidos especificados.
    
    Args:
    - df (DataFrame): Dados originais.
    - partidos (list): Lista de partidos para filtragem.
    
    Retorna:
    - DataFrame: Dados filtrados.
    """
    if not partidos:  # Se a lista de partidos estiver vazia, retorne todos os dados.
        return df
    return df[df['Partido'].isin(partidos)]

def normalizar_arestas(df_grafo, df_politicos):
    """
    Normaliza o peso das arestas com base nas votações.
    
    Args:
    - df_grafo (DataFrame): Dados do grafo.
    - df_politicos (DataFrame): Dados dos políticos.
    
    Retorna:
    - DataFrame: Dados do grafo com pesos normalizados.
    """
    # Mapeando o número de votações para cada deputado
    votacoes = df_politicos.set_index('Nome')['Votacoes'].to_dict()
    
    # Função para calcular o peso normalizado
    def calcular_peso(row):
        votacoes_a = votacoes.get(row['DeputadoA'], None)
        votacoes_b = votacoes.get(row['DeputadoB'], None)
        
        # Se algum deputado não estiver no dicionário, retornar NaN
        if votacoes_a is None or votacoes_b is None:
            return np.nan
        
        return row['Concordancias'] / min(votacoes_a, votacoes_b)
    
    df_grafo['PesoNormalizado'] = df_grafo.apply(calcular_peso, axis=1)
    
    # Remover linhas com NaN (deputados não encontrados no df_politicos)
    df_grafo.dropna(subset=['PesoNormalizado'], inplace=True)
    
    return df_grafo


def filtrar_por_threshold(df, threshold):
    """
    Filtra os dados do grafo com base no threshold especificado.
    
    Args:
    - df (DataFrame): Dados do grafo.
    - threshold (float): Valor mínimo para o peso normalizado.
    
    Retorna:
    - DataFrame: Dados filtrados.
    """
    return df[df['PesoNormalizado'] >= threshold]
