import processamento_grafo as pg
import analise_visualizacao as av

def main():
    # Solicita o ano de análise ao usuário
    ano = int(input("Informe o ano de análise (ex: 2023): "))
    
    # Cria e processa o grafo de votações
    gv = pg.GrafoVotacoes()
    dados_politicos, dados_grafo = gv.carregar_dados(ano)
    gv.criar_grafo(dados_politicos, dados_grafo)
    gv.normalizar_pesos()
    
    # Solicita ao usuário se deseja filtrar por partidos
    filtrar_partidos = input("Deseja filtrar por partidos? (s/n): ").lower()
    if filtrar_partidos == 's':
        partidos = input("Informe os partidos separados por vírgula (ex: MDB,PL): ").split(',')
        gv.filtrar_por_partido(partidos)
    
    # Solicita ao usuário o threshold para filtragem das arestas
    threshold = float(input("Informe o threshold para filtragem das arestas (ex: 0.9): "))
    gv.aplicar_threshold(threshold)
    
    # Inverte os pesos das arestas para cálculo de centralidade
    gv.inverter_pesos()
    
    # Realiza as análises e visualizações
    centralidade = av.calcular_centralidade(gv.grafo)
    
    av.salvar_centralidade(centralidade, ano)
    av.salvar_heatmap(gv.grafo, ano)
    av.salvar_grafo(gv.grafo, ano)

if __name__ == "__main__":
    main()
