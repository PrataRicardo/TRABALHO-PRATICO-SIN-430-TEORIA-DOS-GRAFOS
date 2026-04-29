from grafos_lib.Grafo import Grafo

# Testando como Lista de Adjacência
grafo_lista = Grafo(tipo_representacao='lista')
grafo_lista.carregar_arquivo('entradas/grafo_teste.txt')
print("Lista de Adjacência:", getattr(grafo_lista, 'lista_adj'))

# Testando como Matriz de Adjacência
grafo_matriz = Grafo(tipo_representacao='matriz')
grafo_matriz.carregar_arquivo('entradas/grafo_teste.txt')
print("\nMatriz de Adjacência:")
for linha in grafo_matriz.matriz_adj:
    print(linha)

grafo_lista.gerar_relatorio_saida('saidas/relatorio_teste.txt')

print("\n--- Testando Busca em Largura (BFS) ---")
pais, niveis = grafo_lista.bfs(1)
print("Pais:", pais)
print("Níveis:", niveis)
grafo_lista.gerar_saida_busca('saidas/saida_bfs.txt', pais, niveis)

print("\n--- Testando Busca em Profundidade (DFS) ---")
# Iniciando a busca também a partir do vértice 1
pais_dfs, niveis_dfs = grafo_lista.dfs(vertice_inicial=1)

print("Pais DFS:", pais_dfs)
print("Níveis DFS:", niveis_dfs)
grafo_lista.gerar_saida_busca('saidas/saida_dfs.txt', pais_dfs, niveis_dfs)

print("\n--- Testando Distâncias e Diâmetro ---")

dist_1_3 = grafo_lista.distancia(1, 3)
dist_1_5 = grafo_lista.distancia(1, 5)
dist_3_4 = grafo_lista.distancia(3, 4)

print(f"Distância entre 1 e 3: {dist_1_3}")
print(f"Distância entre 1 e 5: {dist_1_5}")
print(f"Distância entre 3 e 4: {dist_3_4}")

diametro_ex = grafo_lista.diametro_exato()
diametro_aprox = grafo_lista.diametro_aproximado()

print(f"Diâmetro Exato: {diametro_ex}")
print(f"Diâmetro Aproximado: {diametro_aprox}")

print("\n--- Testando Componentes Conexas ---")
comps = grafo_lista.componentes_conexas()
print(f"Total de Componentes: {len(comps)}")
for i, c in enumerate(comps, 1):
    print(f"Tamanho da Componente {i}: {len(c)}")
    print(f"Vértices: {c}")

grafo_lista.gerar_relatorio_saida('saidas/relatorio_completo_teste.txt')