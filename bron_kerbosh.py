import networkx as nx
import matplotlib.pyplot as plt


def bron_kerbosch(R, P, X, graph, cliques):
    """
    Алгоритм Брона-Кербоша для поиска максимальных клик.

    Параметры:
    R - текущее множество вершин в клике
    P - кандидаты на расширение клики
    X - уже обработанные вершины, которые не могут быть
    в текущей клике
    graph - граф (объект NetworkX)
    cliques - список всех найденных максимальных клик
    """
    if not P and not X:
        cliques.append(R)
        return

    for vertex in P.copy():
        bron_kerbosch(R.union({vertex}),
                      P.intersection(set(graph.neighbors(vertex))),
                      X.intersection(set(graph.neighbors(vertex))),
                      graph,
                      cliques)
        P.discard(vertex)
        X.add(vertex)


def find_maximal_cliques(graph):
    """
    Нахождение всех максимальных клик в графе.

    Параметры:
    :param graph: граф (объект NetworkX)

    Возвращает:
    :return: список всех максимальных клик
    """
    cliques = []
    P = set(graph.nodes())
    bron_kerbosch(set(), P, set(), graph, cliques)
    return cliques


def visualize_graph(graph, cliques):
    """
    Визуализация графа и его максимальных клик.

    Параметры:
    :param graph: граф (объект NetworkX)
    :param cliques: список максимальных клик
    """
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))

    # Рисуем граф
    nx.draw(graph, pos, with_labels=True, node_color='lightblue',
            node_size=3000, font_size=15, font_weight='bold')

    # Раскраска клик
    colors = ['red', 'green', 'blue', 'orange', 'purple']
    for i, clique in enumerate(cliques):
        nx.draw_networkx_nodes(graph, pos, nodelist=clique,
                               node_color=colors[i % len(colors)], node_size=3000,
                               alpha=0.6)

    plt.title("Граф и его максимальные клики")
    plt.show()


# Создание графа
G = nx.Graph()
edges = [(1, 2), (1, 3), (2, 3), (3, 4)]
G.add_edges_from(edges)

G2 = nx.Graph()
edges2 = [(1, 5), (1, 2), (2, 5), (2, 3), (5, 4), (3, 4), (4, 6)]
G2.add_edges_from(edges2)

# Нахождение максимальных клик
maximal_cliques = find_maximal_cliques(G)
print("Максимальные клики:", maximal_cliques)

maximal_cliques2 = find_maximal_cliques(G2)
print("Максимальные клики:", maximal_cliques2)

# Визуализация графа и клик
visualize_graph(G, maximal_cliques)
visualize_graph(G2, maximal_cliques2)