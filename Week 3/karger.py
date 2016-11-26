import random
import math
import copy
from joblib import Parallel, delayed
import multiprocessing
import time


def contract_randomly(graph):
    while len(graph) > 2:
        u, v = pick_random_edge(graph)
        merge_and_remove_loops(graph, u, v)
    key = list(graph.keys())[0]
    return len(graph[key])


def pick_random_edge(graph):
    u = random.choice(list(graph.keys()))
    v = random.choice(graph[u])
    return u, v


def merge_and_remove_loops(graph, u, v):
    for node in graph[u]:
        if node != v:  # remove self loops
            graph[v].append(node)  # u's nodes now adjacent to v
            graph[node].append(v)
        graph[node].remove(u)
    del graph[u]


def parallel_contraction(graph, N):
    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(contract_randomly)(copy.deepcopy(graph))
                                         for i in range(N))
    return min(results)


def determine_min_cut(graph, N):
    min_cut = math.inf
    for iteration in range(N):
        tmp = contract_randomly(copy.deepcopy(graph))
        if tmp < min_cut:
            min_cut = tmp
    return min_cut


if __name__ == '__main__':
    graph = {}
    with open('kargerMinCut.txt') as data:
        for line in data:
            spl = line.split()
            if spl:
                node, edges = spl[0], spl[1:]
                graph[node] = edges
    start_time = time.time()
    print(parallel_contraction(graph, 10000))
    print(time.time() - start_time)
