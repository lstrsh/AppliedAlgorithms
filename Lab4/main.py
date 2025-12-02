import time
import random

class UnionFind:
    def __init__(self, n):
        self.reps = [i for i in range(n)]
        self.sets = {i: [i] for i in range(n)}

    def find(self, x):
        return self.reps[x]

    def union(self, x, y):
        rx, ry = self.reps[x], self.reps[y]
        if rx == ry:
            return False
        set_x, set_y = self.sets[rx], self.sets[ry]
        if len(set_x) < len(set_y):
            small, large = set_x, set_y
            s_rep, l_rep = rx, ry
        else:
            small, large = set_y, set_x
            s_rep, l_rep = ry, rx
        for node in small:
            self.reps[node] = l_rep
        large.extend(small)
        del self.sets[s_rep]
        return True

def kruskal(n, edges):
    edges.sort(key=lambda e: e[2])
    uf = UnionFind(n)
    mst = []
    weight = 0
    start = time.perf_counter()
    for u, v, w in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, w))
            weight += w
    end = time.perf_counter()
    return mst, weight, end - start

def generate_graph(n):
    edges = []
    for i in range(n-1):
        edges.append((i, i+1, random.randint(1,100)))
    max_edges = n*(n-1)//2
    target = int(max_edges * 0.1)
    while len(edges) < target:
        u, v = random.randint(0, n-1), random.randint(0, n-1)
        if u != v:
            edges.append((u, v, random.randint(1,100)))
    return edges

def tst():
    print(f"{'v':<5} {'e':<7} {'time/sec':<10}")
    vertex_counts = [100, 500, 1000, 2000, 3000]
    for n in vertex_counts:
        edges = generate_graph(n)
        mst, w, t = kruskal(n, edges)
        print(f'{n:<5} {len(edges):<7} {t:.6f}')

if __name__ == '__main__':
    test_n = 4
    test_edges = [
        (0,1,10),
        (0,2,6),
        (0,3,5),
        (1,3,15),
        (2,3,4)
    ]
    mst, weight, a = kruskal(test_n, test_edges)
    tst()
