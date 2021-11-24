import networkx as nx
import timeit
import matplotlib.pyplot as plt
import math

def MakeSet(x):
    x.parent = x
    x.rank = 0

def Union(x, y):
    xRoot = Find(x)
    yRoot = Find(y)
    if xRoot.rank > yRoot.rank:
        yRoot.parent = xRoot
    elif xRoot.rank < yRoot.rank:
        xRoot.parent = yRoot
    elif xRoot != yRoot:
        yRoot.parent = xRoot
        xRoot.rank = xRoot.rank + 1

def Find(x):
    if x.parent == x:
        return x
    else:
        x.parent = Find(x.parent)
        return x.parent

class Node:
    def __init__ (self, label):
        self.label = label
    def __str__(self):
        return self.label

def show_figure(data):
    plt.figure(figsize=(9,9))
    plt.title('Dependence of the running time on the number of vertices')
    plt.xlabel('Number of vertices')
    plt.ylabel('Running time')
    plt.grid()

    x = []
    y = []
    for exp in data:
        x.append(exp['size'])
        y.append(exp['time'])

    plt.plot(x, y)
    plt.show()

def test_kruskal(n):
    # Тестируем алгоритм Краскала
    sizes = [64*n + 16*i*n for i in range(17)]
    i = 0
    tests = []
    for k in range(len(sizes)):
        tests.append({'size': sizes[k], 'equal': False})
    for size in sizes:
        time = 0
        # Генерируем произвольный граф
        g = weighted_complete_graph(size,1,10000)
        # Считаем минимальное остовное дерево с помощью
        # функции из библиотеки
        T = nx.minimum_spanning_tree(g)
        # Сортируем рёбра по весу
        edges = list(T.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'])
        # Считаем усреднённое время за 20 итераций алгоритма для каждого N
        for j in range(20):
            start = timeit.default_timer()
            if compare(kruskalDUS(g),edges):
                tests[i]['equal'] = True
            else:
                tests[i]['equal'] = False
            stop = timeit.default_timer()
            time += stop-start
        tests[i]['time'] = time / 20
        i += 1
    return tests

def weighted_complete_graph(n, lower_weight, upper_weight):
    # Генерируем граф из n вершин с произвольными весами
    import random
    g = nx.complete_graph(n)
    m = len(list(g.edges))
    weights = [random.randint(lower_weight, upper_weight) for r in range(m)]
    i = 0
    for edge in list(g.edges):
        g[edge[0]][edge[1]]['weight'] = weights[i]
        i += 1
    return g

def kruskalDUS(g):
    # Сортируем рёбра по весу
    edges = list(g.edges(data=True))
    edges.sort(key=lambda x: x[2]['weight'])
    # Создаём систему непересекающихся множеств
    comp = [Node(str(x)) for x in range(len(list(g.nodes)))]
    [MakeSet(node) for node in comp]
    res = []
    for edge in edges:
        start = edge[0]
        end = edge[1]
        # Если концы рёбер лежат в разных  множествах, то объединяем эти множества
        if str(Find(comp[start])) != str(Find(comp[end])):
            weight = edge[2]['weight']
            res.append((start,end, {'weight': weight}))
            a = comp[start]
            b = comp[end]
            Union(a,b)
    return res



def compare(g1,g2):
    # сравниваем деревья полученные функцией из библиотеки и
    # алгоритмом Краскала
    if len(g1) != len(g2):
        return False
    for i in range(len(g1)):
        for j in range(len(g1[i])):
            if j == 2:
                if g1[i][j]['weight'] != g2[i][j]['weight']:
                    return False
            if g1[i][j] != g2[i][j]:
                return False
    return True

def find_relation(g1,g2):
    # Считаем отношение времени работы T(2n) к T(n)
    res = []
    for i in range(len(g2)):
        res.append(g2[i]['time'] / g1[i]['time'])
    return res

tn = test_kruskal(1)
t2n = test_kruskal(2)

print(tn)
print(t2n)
print(find_relation(tn, t2n))
show_figure(tn)
