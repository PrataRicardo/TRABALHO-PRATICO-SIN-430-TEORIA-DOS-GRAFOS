import statistics
from collections import deque

class Grafo:
    def __init__(self, tipo_representacao='lista'):
        """
        tipo_representacao: 'lista' para Lista de Adjacência ou 'matriz' para Matriz de Adjacência.
        """
        self.tipo_representacao = tipo_representacao
        self.num_vertices = 0
        self.num_arestas = 0
        
        self.lista_adj = {}
        self.matriz_adj = []

    def carregar_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
            
        self.num_vertices = int(linhas[0].strip())
        # O número de arestas é a quantidade de linhas restantes
        self.num_arestas = len(linhas) - 1
        
        # Inicializa a estrutura escolhida
        if self.tipo_representacao == 'matriz':
            # Cria uma matriz N x N preenchida com zeros
            self.matriz_adj = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        else:
            # Cria um dicionário onde cada chave é um vértice (de 1 a N) com uma lista vazia
            self.lista_adj = {i: [] for i in range(1, self.num_vertices + 1)}
            
        # Percorre as linhas subsequentes que contêm as arestas
        for linha in linhas[1:]:
            u, v = map(int, linha.strip().split())
            self._adicionar_aresta(u, v)

    def _adicionar_aresta(self, u, v):
        if self.tipo_representacao == 'matriz':
            # Subtrai 1 pois o arquivo usa vértices 1, mas arrays em Python começa em 0
            self.matriz_adj[u-1][v-1] = 1
            self.matriz_adj[v-1][u-1] = 1
        else:
            self.lista_adj[u].append(v)
            self.lista_adj[v].append(u)

    def obter_graus(self):
        """
        Retorna uma lista com o grau de cada vértice, 
        independentemente da representação escolhida.
        """
        graus = []
        if self.tipo_representacao == 'lista':
            # O grau na lista de adjacência é o tamanho da lista de vizinhos
            for vizinhos in self.lista_adj.values():
                graus.append(len(vizinhos))
        else:
            # Na matriz, o grau é a soma dos '1's na linha do vértice
            for linha in self.matriz_adj:
                graus.append(sum(linha))
        return graus

    def gerar_relatorio_saida(self, caminho_saida):
        """
        Gera o arquivo de texto com as estatísticas exigidas pelo trabalho.
        """
        graus = self.obter_graus()
        
        grau_minimo = min(graus)
        grau_maximo = max(graus)
        grau_medio = sum(graus) / self.num_vertices
        mediana_grau = statistics.median(graus)

        componentes = self.componentes_conexas()

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(f"Número de vértices: {self.num_vertices}\n")
            f.write(f"Número de arestas: {self.num_arestas}\n")
            f.write(f"Grau mínimo: {grau_minimo}\n")
            f.write(f"Grau máximo: {grau_maximo}\n")
            f.write(f"Grau médio: {grau_medio:.2f}\n")
            f.write(f"Mediana de grau: {mediana_grau}\n")
            
            # componentes conexas
            f.write("\n--- Componentes Conexas ---\n")
            f.write(f"Total de componentes: {len(componentes)}\n")
            
            for i, comp in enumerate(componentes, 1):
                f.write(f"Componente {i} -> Tamanho: {len(comp)} vértices | Vértices: {comp}\n")

    def bfs(self, vertice_inicial):
        """
        Executa a Busca em Largura (BFS) a partir de um vértice inicial.
        Retorna dois dicionários: pais e níveis dos vértices.
        """
        # Inicialização das estruturas
        visitados = set()
        pais = {i: None for i in range(1, self.num_vertices + 1)}
        niveis = {i: -1 for i in range(1, self.num_vertices + 1)} # -1 indica não alcançado
        
        fila = deque()
        
        # Configura a raiz
        visitados.add(vertice_inicial)
        niveis[vertice_inicial] = 0
        fila.append(vertice_inicial)
        
        # Execução da busca
        while fila:
            u = fila.popleft()
            
            # Resgata os vizinhos do vértice atual dependendo da representação escolhida
            if self.tipo_representacao == 'lista':
                vizinhos = self.lista_adj[u]
            else:
                # Na matriz, pega o índice (v+1) apenas onde o valor for 1
                vizinhos = [v + 1 for v, conectado in enumerate(self.matriz_adj[u - 1]) if conectado == 1]
                
            for v in vizinhos:
                if v not in visitados:
                    visitados.add(v)
                    pais[v] = u
                    niveis[v] = niveis[u] + 1
                    fila.append(v)
                    
        return pais, niveis

    def gerar_saida_busca(self, caminho_saida, pais, niveis):
        """
        Grava o resultado da busca (pai e nível) em um arquivo texto.
        """
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write("Vertice | Pai | Nivel\n")
            f.write("-" * 25 + "\n")
            for vertice in range(1, self.num_vertices + 1):
                pai = pais[vertice] if pais[vertice] is not None else '-'
                nivel = niveis[vertice] if niveis[vertice] != -1 else '-'
                f.write(f"{vertice:7} | {str(pai):3} | {str(nivel):5}\n")

    def dfs(self, vertice_inicial):
        """
        Executa a Busca em Profundidade (DFS) a partir de um vértice inicial.
        Utiliza uma abordagem iterativa com pilha para suportar grafos grandes.
        Retorna dois dicionários: pais e níveis dos vértices.
        """
        visitados = set()
        pais = {i: None for i in range(1, self.num_vertices + 1)}
        niveis = {i: -1 for i in range(1, self.num_vertices + 1)}
        
        # A pilha guarda tuplas no formato: (vertice_atual, pai, nivel)
        pilha = [(vertice_inicial, None, 0)]
        
        while pilha:
            u, pai, nivel = pilha.pop()
            
            if u not in visitados:
                visitados.add(u)
                pais[u] = pai
                niveis[u] = nivel
                
                # Resgata os vizinhos
                if self.tipo_representacao == 'lista':
                    vizinhos = self.lista_adj[u]
                else:
                    vizinhos = [v + 1 for v, conectado in enumerate(self.matriz_adj[u - 1]) if conectado == 1]
                
                # Invertemos a ordem dos vizinhos na hora de colocar na pilha.
                # Isso garante que o primeiro vizinho numérico seja explorado primeiro
                # (já que ele ficará no topo da pilha), simulando o comportamento recursivo padrão.
                for v in reversed(vizinhos):
                    if v not in visitados:
                        pilha.append((v, u, nivel + 1))
                        
        # Como o vértice inicial é a raiz, garantimos que o pai dele é None
        pais[vertice_inicial] = None 
        
        return pais, niveis
    
    def distancia(self, u, v):
        """
        Calcula a menor distância entre os vértices u e v usando BFS.
        """
        _, niveis = self.bfs(u)
        dist = niveis[v]
        return dist if dist != -1 else float('inf') # Retorna infinito se não houver caminho

    def diametro_exato(self):
        """
        Calcula o diâmetro exato rodando BFS para todos os vértices.
        Cuidado: Pode ser muito lento em grafos grandes.
        """
        max_dist = 0
        for i in range(1, self.num_vertices + 1):
            _, niveis = self.bfs(i)
            # Ignora os -1 (vértices inalcançáveis)
            distancias_validas = [d for d in niveis.values() if d != -1]
            if distancias_validas:
                max_nivel = max(distancias_validas)
                if max_nivel > max_dist:
                    max_dist = max_nivel
        return max_dist

    def diametro_aproximado(self):
        """
        Calcula uma aproximação do diâmetro usando a heurística de 2 BFS.
        Muito mais rápido para os estudos de caso com grafos grandes.
        """
        import random
        
        # Escolhe um vértice aleatório e roda a primeira BFS
        v_aleatorio = random.randint(1, self.num_vertices)
        _, niveis_1 = self.bfs(v_aleatorio)
        
        # Encontra o vértice mais distante alcançável
        v_mais_distante = v_aleatorio
        maior_dist = -1
        for vertice, dist in niveis_1.items():
            if dist > maior_dist:
                maior_dist = dist
                v_mais_distante = vertice
                
        # Roda a segunda BFS a partir desse vértice extremo
        _, niveis_2 = self.bfs(v_mais_distante)
        
        # A maior distância encontrada agora é o nosso diâmetro aproximado
        return max([d for d in niveis_2.values() if d != -1])
    
    def componentes_conexas(self):
        """
        Descobre as componentes conexas do grafo.
        Retorna uma lista de componentes (cada componente é uma lista de vértices),
        ordenada em ordem decrescente de tamanho.
        """
        visitados_globais = set()
        componentes = []

        for i in range(1, self.num_vertices + 1):
            if i not in visitados_globais:
                # Se não foi visitado, é uma nova componente. Rodamos a BFS para mapeá-la.
                _, niveis = self.bfs(i)
                
                # Todos os vértices que receberam um nível diferente de -1 foram alcançados
                componente_atual = [v for v, nivel in niveis.items() if nivel != -1]
                
                # Registramos esses vértices como visitados globalmente
                visitados_globais.update(componente_atual)
                
                # Salvamos a componente encontrada
                componentes.append(componente_atual)

        # O trabalho exige listar em ordem decrescente de tamanho
        componentes.sort(key=len, reverse=True)
        return componentes