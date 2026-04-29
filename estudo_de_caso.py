import time
import tracemalloc
import random
import os
from grafos_lib.Grafo import Grafo

def estimar_memoria_matriz(num_vertices):
    """
    Calcula a estimativa de RAM necessária para a matriz em Python.
    No Python, uma lista de listas com inteiros usa internamente ponteiros de 64-bits (8 bytes).
    Isso é uma estimativa conservadora (o overhead de listas aninhadas no Python é ainda maior).
    """
    bytes_necessarios = (num_vertices ** 2) * 8
    gb_necessarios = bytes_necessarios / (1024 ** 3)
    return gb_necessarios

def testar_carregamento(caminho_arquivo, representacao):
    print(f"\n--- [1] Teste de Memória: {representacao.upper()} ---")
    
    # Lendo apenas a primeira linha para obter os vértices e estimar o tamanho
    with open(caminho_arquivo, 'r') as f:
        num_vertices = int(f.readline().strip())
        
    if representacao == 'matriz':
        gb_estimado = estimar_memoria_matriz(num_vertices)
        print(f"Teoria: Matriz {num_vertices}x{num_vertices} precisará de pelo menos {gb_estimado:.2f} GB de RAM.")
        if gb_estimado > 14.0:
            print(f"Alerta: Alocação ignorada para proteger o SO. O tempo estimado para falha por paginação seria de horas.")
            return None

    tracemalloc.start()
    tempo_inicio = time.perf_counter()
    
    grafo = Grafo(tipo_representacao=representacao)
    try:
        grafo.carregar_arquivo(caminho_arquivo)
        tempo_fim = time.perf_counter()
        
        _, pico_memoria = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        memoria_mb = pico_memoria / (1024 * 1024)
        print(f"Sucesso! Memória RAM alocada: {memoria_mb:.2f} MB")
        print(f"Tempo de I/O para montar a estrutura: {tempo_fim - tempo_inicio:.2f}s")
        return grafo
        
    except MemoryError:
        tempo_fim = time.perf_counter()
        tracemalloc.stop()
        print(f"FALHA: MemoryError levantado após {tempo_fim - tempo_inicio:.2f}s tentando alocar a memória.")
        return None

def rodar_estudos_completos(caminho_arquivo):
    print("\n" + "="*70)
    print(f"ESTUDO DE CASO: {os.path.basename(caminho_arquivo)}")
    print("="*70)
    
    # ==========================================
    # QUESTÃO 1: MEMÓRIA
    # ==========================================
    # Tentativa com Lista
    grafo = testar_carregamento(caminho_arquivo, 'lista')
    if not grafo:
        print("Erro crítico: Não foi possível carregar nem a Lista de Adjacência.")
        return
        
    # Tentativa com Matriz
    testar_carregamento(caminho_arquivo, 'matriz')

    # ==========================================
    # QUESTÕES 2 E 3: TEMPO MÉDIO DE 100 BUSCAS
    # ==========================================
    print("\n--- [2 e 3] Teste de Tempo Médio (100 Execuções) ---")
    
    # Para 100 execuções partindo de vértices diferentes, 
    # sorteamos 100 vértices aleatórios entre 1 e N.
    vertices_sorteados = [random.randint(1, grafo.num_vertices) for _ in range(100)]
    
    # 100x BFS
    inicio_bfs_total = time.perf_counter()
    for v in vertices_sorteados:
        grafo.bfs(v)
    tempo_medio_bfs = (time.perf_counter() - inicio_bfs_total) / 100
    print(f"Tempo médio de 1 BFS: {tempo_medio_bfs:.5f} segundos")
    
    # 100x DFS
    inicio_dfs_total = time.perf_counter()
    for v in vertices_sorteados:
        grafo.dfs(v)
    tempo_medio_dfs = (time.perf_counter() - inicio_dfs_total) / 100
    print(f"Tempo médio de 1 DFS: {tempo_medio_dfs:.5f} segundos")

    # ==========================================
    # QUESTÃO 4: PAIS DE 10, 20 E 30
    # ==========================================
    print("\n--- [4] Pais na Árvore Geradora ---")
    alvos = [10, 20, 30]
    for inicio in [1, 2, 3]:
        pais_bfs, _ = grafo.bfs(inicio)
        pais_dfs, _ = grafo.dfs(inicio)
        
        pais_bfs_formatados = {alvo: pais_bfs.get(alvo, 'N/A') for alvo in alvos}
        pais_dfs_formatados = {alvo: pais_dfs.get(alvo, 'N/A') for alvo in alvos}
        
        print(f"  Origem {inicio} | BFS -> Pais: {pais_bfs_formatados}")
        print(f"  Origem {inicio} | DFS -> Pais: {pais_dfs_formatados}")

    # ==========================================
    # QUESTÃO 5: DISTÂNCIAS
    # ==========================================
    print("\n--- [5] Distâncias ---")
    for u, v in [(10, 20), (10, 30), (20, 30)]:
        print(f"  Distância ({u} -> {v}): {grafo.distancia(u, v)}")

    # ==========================================
    # QUESTÃO 6: COMPONENTES CONEXAS
    # ==========================================
    print("\n--- [6] Componentes Conexas ---")
    comps = grafo.componentes_conexas()
    print(f"  Quantidade de Componentes: {len(comps)}")
    print(f"  Tamanho da Maior Componente: {len(comps[0])} vértices")
    print(f"  Tamanho da Menor Componente: {len(comps[-1])} vértices")

    # ==========================================
    # QUESTÃO 7: DIÂMETRO (APROXIMADO)
    # ==========================================
    print("\n--- [7] Diâmetro ---")
    print(f"  Diâmetro Aproximado (Heurística): {grafo.diametro_aproximado()}")
    print("-" * 70)

# Executando para uma lista de arquivos.
arquivos = [
    'entradas/grafo_1.txt',
    # 'entradas/grafo_2.txt', 
    # 'entradas/grafo_3.txt',
    # 'entradas/grafo_4.txt',
    # 'entradas/grafo_5.txt',
]

for arq in arquivos:
    if os.path.exists(arq):
        rodar_estudos_completos(arq)
    else:
        print(f"\nArquivo {arq} não encontrado na pasta.")