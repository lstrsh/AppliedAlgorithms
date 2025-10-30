import random
import time
import sys
import matplotlib.pyplot as plt


sys.setrecursionlimit(20000)

def gen_graph(n, p, seed=None):
    if seed is not None: random.seed(seed)

    g = [[0] * n for z in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:continue
            if random.random() < p: g[i][j] = 1

    return g


def matrix_to_list(mat):
    n = len(mat)
    adj_list = [[] for z in range(n)]
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                adj_list[i].append(j)
    return adj_list


def dfs_matrix(mat, v, visited):
    visited[v] = True
    n = len(mat)
    for u in range(n):
        if mat[v][u] == 1 and not visited[u]:
            dfs_matrix(mat, u, visited)


def is_connected_dfs_matrix(mat):
    n = len(mat)
    if n == 0: return True

    for start_node in range(n):
        visited = [False] * n
        dfs_matrix(mat, start_node, visited)
        if not all(visited): return False
    return True

def dfs_list(adj, v, visited):
    visited[v] = True
    for u in adj[v]:
        if not visited[u]:
            dfs_list(adj, u, visited)


def is_conn_dfs_list(adj):
    n = len(adj)
    if n == 0: return True

    for start_node in range(n):
        visited = [False] * n
        dfs_list(adj,start_node, visited)
        if not all(visited): return False
    return True


def warshall(mat):
    n = len(mat)
    reach = [row[:] for row in mat]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return reach


def is_conn_warshall(mat):
    reach = warshall(mat)
    n = len(reach)
    if n == 0:return True

    for i in range(n):
        for j in range(n):
            if i == j: continue
            if not reach[i][j]: return False
    return True

def get_time(func, *args):
    t0 = time.perf_counter()
    func(*args)
    t1 = time.perf_counter()

    return t1-t0


def comparison(ns, ps, reps):
    results = []

    for n in ns:
        for p in ps:

            t_dfs_m, t_dfs_l, t_war = [], [], []

            for r in range(reps):
                g_matrix = gen_graph(n, p)

                g_list = matrix_to_list(g_matrix)

                td_m = get_time(is_connected_dfs_matrix, g_matrix)
                td_l = get_time(is_conn_dfs_list, g_list)
                tw = get_time(is_conn_warshall, g_matrix)

                t_dfs_m.append(td_m)
                t_dfs_l.append(td_l)
                t_war.append(tw)

            avg_dfs_m, avg_dfs_l, avg_war = sum(t_dfs_m)/len(t_dfs_m), sum(t_dfs_l)/len(t_dfs_l), sum(t_war)/len(t_war)
            results.append((n, p, avg_dfs_m, avg_dfs_l, avg_war))
            print(f'n={n:3d}, p={p:.2f} - DFS matrics={avg_dfs_m:.6f}sec - DFS lists={avg_dfs_l:.6f}sec - Warshall={avg_war:.6f}sec')
    return results


def plot_res(results):
    grouped = {}
    for (n, p, tdfs_m, tdfs_l, twar) in results:
        grouped.setdefault(n, []).append((p, tdfs_m, tdfs_l, twar))
    for n, rows in grouped.items():
        ps = [x[0] for x in rows]
        dfs_m_times, dfs_l_times, war_times = [x[1] for x in rows], [x[2] for x in rows], [x[3] for x in rows]

        plt.figure(figsize=(10, 6))
        plt.plot(ps, dfs_m_times, marker='o', label='DFS через матрицю')
        plt.plot(ps, dfs_l_times, marker='s', label='DFS через списки суміжності')
        plt.plot(ps, war_times, marker='x', linestyle='--', label='Алгоритм Уоршелла')
        plt.title(f'Час роботи n={n}')
        plt.xlabel('Щільність')
        plt.ylabel('секунди')
        plt.legend()
        plt.grid(True)
        plt.show()


ns = [50, 100, 150, 200]
ps = [0.01, 0.05, 0.1, 0.2, 0.3]
plot_res(comparison(ns, ps, reps=100))
