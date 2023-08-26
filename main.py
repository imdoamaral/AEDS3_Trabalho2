"""
Análise de Proximidade na Câmara de Deputados

Descrição:
Este projeto analisa as relações de proximidade entre deputados na Câmara dos Deputados do Brasil.
Através de uma interface gráfica, o usuário pode definir parâmetros específicos para a análise.
O programa gera três tipos principais de visualizações:
    1. Centralidade de Betweenness: Mostra a importância dos deputados como "pontes" na rede.
    2. Heatmap: Representa a correlação entre os deputados com base em suas concordâncias.
    3. Grafo de Conexões: Visualiza as conexões entre deputados.

Dependências:
    - pandas: Para manipulação e análise de dados.
    - numpy: Suporte para arrays e funções matemáticas.
    - networkx: Para criação, manipulação e estudo da estrutura de redes complexas.
    - matplotlib: Para criação de visualizações/gráficos.
    - seaborn: Para melhoria na visualização de gráficos e plots estatísticos.
    - tkinter: Para a interface gráfica do usuário.

Comando para Instalação das Dependências:
    pip install pandas numpy networkx matplotlib seaborn

Autores:
    Henrique Barcelos Saraiva - 19.2.8007
    Israel Matias do Amaral - 18.1.8050

"""

import dados
import graficos
import interface

def main():
    # Coletar entradas do usuário
    user_inputs = interface.coletar_inputs()

    ano = int(user_inputs['ano'])
    partidos = user_inputs['partidos']
    threshold = user_inputs['threshold']

    # Ler e filtrar dados
    df_politicos = dados.ler_politicos(ano)
    df_politicos = dados.filtrar_partidos(df_politicos, partidos)

    df_grafo = dados.ler_grafo(ano)
    df_grafo = dados.normalizar_arestas(df_grafo, df_politicos)
    df_grafo = dados.filtrar_por_threshold(df_grafo, threshold)

    # Gerar e plotar gráficos
    graficos.criar_pasta_resultados()
    
    G = graficos.gerar_grafo(df_grafo)
    graficos.plotar_centralidade(G, ano, partidos, threshold, df_politicos)
    graficos.plotar_grafo(G, ano, partidos, df_politicos, threshold)
    graficos.plotar_heatmap(df_grafo, ano, partidos, threshold, df_politicos)

    # Exibir mensagem de conclusão
    interface.exibir_mensagem("Conclusão", "Análise concluída e gráficos gerados na pasta 'resultados'.")

if __name__ == "__main__":
    main()