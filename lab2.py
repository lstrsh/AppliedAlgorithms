from abc import ABC, abstractmethod
import random
import matplotlib.pyplot as plt
import networkx as nx


class Graph(ABC):
    def __init__(self, n=0, use_matrix=True):
        self.n = n
        self.use_matrix = use_matrix
        if use_matrix:
            self.data = [[0 for _ in range(n)] for _ in range(n)]
        else:
            self.data = {i: [] for i in range(n)}

    @abstractmethod
    def add_edge(self, u, v, w=None):
        pass

    @abstractmethod
    def remove_edge(self, u, v):
        pass

    def add_vertex(self):
        self.n += 1
        if self.use_matrix:
            for row in self.data:
                row.append(0)
            self.data.append([0] * self.n)
        else:
            self.data[self.n - 1] = []

    def remove_vertex(self, v):
        if v < 0 or v >= self.n:
            return
        if self.use_matrix:
            self.data.pop(v)
            for row in self.data:
                row.pop(v)
        else:
            self.data.pop(v, None)
            for key in list(self.data.keys()):
                self.data[key] = [x for x in self.data[key] if x != v]
        self.n -= 1

    def convert(self):
        if self.use_matrix:
            adj = {}
            for i in range(self.n):
                adj[i] = []
                for j in range(self.n):
                    if self.data[i][j] != 0:
                        adj[i].append(j)
            self.data = adj
            self.use_matrix = False
        else:
            mat = [[0 for _ in range(self.n)] for _ in range(self.n)]
            for i, neigh in self.data.items():
                for j in neigh:
                    mat[i][j] = 1
            self.data = mat
            self.use_matrix = True

    def degree(self, v):
        if self.use_matrix:
            return sum(1 for x in self.data[v] if x != 0)
        else:
            return len(self.data[v])

    def isolated_vertices(self):
        return [i for i in range(self.n) if self.degree(i) == 0]

    def pendant_vertices(self):
        return [i for i in range(self.n) if self.degree(i) == 1]

    def __str__(self):
        return f'Graph(n={self.n}, matrix={self.use_matrix})\n{self.data}'


class UndirectedGraph(Graph):
    def add_edge(self, u, v, w=None):
        if u >= self.n or v >= self.n:
            return
        val = w if w is not None else 1
        if self.use_matrix:
            self.data[u][v] = val
            self.data[v][u] = val
        else:
            if v not in self.data[u]:
                self.data[u].append(v)
            if u not in self.data[v]:
                self.data[v].append(u)

    def remove_edge(self, u, v):
        if self.use_matrix:
            self.data[u][v] = 0
            self.data[v][u] = 0
        else:
            if v in self.data[u]:
                self.data[u].remove(v)
            if u in self.data[v]:
                self.data[v].remove(u)


class DirectedGraph(Graph):
    def add_edge(self, u, v, w=None):
        if u >= self.n or v >= self.n:
            return
        val = w if w is not None else 1
        if self.use_matrix:
            self.data[u][v] = val
        else:
            if v not in self.data[u]:
                self.data[u].append(v)

    def remove_edge(self, u, v):
        if self.use_matrix:
            self.data[u][v] = 0
        else:
            if v in self.data[u]:
                self.data[u].remove(v)


class WeightedGraph(UndirectedGraph):
    def add_edge(self, u, v, w=1):
        super().add_edge(u, v, w)


def generate_random_graph(n, p, directed=False, weighted=False, w_min=1, w_max=10, use_matrix=True):
    if weighted:
        G = WeightedGraph(n, use_matrix)
    elif directed:
        G = DirectedGraph(n, use_matrix)
    else:
        G = UndirectedGraph(n, use_matrix)

    for i in range(n):
        for j in range(i + 1, n) if not directed else range(n):
            if i == j:
                continue
            if random.random() < p:
                w = random.randint(w_min, w_max) if weighted else None
                G.add_edge(i, j, w)
    return G


def visualize_graph(G):
    if G.use_matrix:
        G.convert()
    g = nx.DiGraph() if isinstance(G, DirectedGraph) else nx.Graph()
    for u, neighs in G.data.items():
        for v in neighs:
            if isinstance(v, tuple):
                g.add_edge(u, v[0], weight=v[1])
            else:
                g.add_edge(u, v)
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, node_color='lightblue')
    labels = nx.get_edge_attributes(g, 'weight')
    if labels:
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.show()


if __name__ == '__main__':
    G = generate_random_graph(5, 0.4, weighted=True)
    print(G)
    print('Isolated:', G.isolated_vertices())
    print('Pendant:', G.pendant_vertices())
    visualize_graph(G)

