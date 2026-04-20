import networkx as nx
import matplotlib.pyplot as plt


def bron_kerbosch(R, P, X, graph, cliques):
    """
    Алгоритм Брона-Кербоша для поиска максимальных клик (базовая в��рсия).

    Параметры:
        R (set): текущее множество вершин в строящейся клике
        P (set): кандидаты на расширение клики
        X (set): уже обработанные вершины (не могут войти в текущую клику)
        graph (nx.Graph): неориентированный граф
        cliques (list): накопленный список найденных максимальных клик
    """
    if not P and not X:
        cliques.append(R)
        return

    for vertex in P.copy():
        neighbors = set(graph.neighbors(vertex))
        bron_kerbosch(
            R.union({vertex}),
            P.intersection(neighbors),
            X.intersection(neighbors),
            graph,
            cliques,
        )
        P.discard(vertex)
        X.add(vertex)


def bron_kerbosch_pivot(R, P, X, graph, cliques):
    """
    Алгоритм Брона-Кербоша с выбором опорной вершины (pivot).
    Оптимизированная версия — сокращает количество рекурсивных вызовов.

    Параметры:
        R (set): текущее множество вершин в строящейся клике
        P (set): кандидаты на расширение клики
        X (set): уже обработанные вершины
        graph (nx.Graph): неориентированный граф
        cliques (list): накопленный список найденных максимальных клик
    """
    if not P and not X:
        cliques.append(R)
        return

    # Выбираем pivot — вершину с максимальным числом связей в P ∪ X
    pivot = max(P | X, key=lambda v: len(set(graph.neighbors(v)) & P))
    pivot_neighbors = set(graph.neighbors(pivot))

    for vertex in (P - pivot_neighbors).copy():
        neighbors = set(graph.neighbors(vertex))
        bron_kerbosch_pivot(
            R.union({vertex}),
            P.intersection(neighbors),
            X.intersection(neighbors),
            graph,
            cliques,
        )
        P.discard(vertex)
        X.add(vertex)


def find_maximal_cliques(graph, use_pivot=True):
    """
    Находит все максимальные клики в неориентированном графе.

    Параметры:
        graph (nx.Graph): граф
        use_pivot (bool): использовать оптимизацию с pivot (по умолчанию True)

    Возвращает:
        list[set]: список всех максимальных клик
    """
    cliques = []
    P = set(graph.nodes())
    algorithm = bron_kerbosch_pivot if use_pivot else bron_kerbosch
    algorithm(set(), P, set(), graph, cliques)
    return cliques


def visualize_graph(graph, cliques, title="Граф и его максимальные клики"):
    """
    Визуализирует граф и выделяет найденные максимальные клики цветом.

    Параметры:
        graph (nx.Graph): граф
        cliques (list[set]): список максимальных клик
        title (str): заголовок графика
    """
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(8, 6))

    nx.draw(
        graph, pos,
        with_labels=True,
        node_color="lightblue",
        node_size=3000,
        font_size=15,
        font_weight="bold",
    )

    colors = ["red", "green", "blue", "orange", "purple"]
    for i, clique in enumerate(cliques):
        nx.draw_networkx_nodes(
            graph, pos,
            nodelist=list(clique),
            node_color=colors[i % len(colors)],
            node_size=3000,
            alpha=0.5,
        )

    plt.title(title)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # --- Пример 1: простой граф ---
    G1 = nx.Graph()
    G1.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])

    cliques1 = find_maximal_cliques(G1)
    print("Граф 1 — максимальные клики:", cliques1)
    visualize_graph(G1, cliques1, title="Граф 1")

    # --- Пример 2: более сложный граф ---
    G2 = nx.Graph()
    G2.add_edges_from([(1, 5), (1, 2), (2, 5), (2, 3), (5, 4), (3, 4), (4, 6)])

    cliques2 = find_maximal_cliques(G2)
    print("Граф 2 — максимальные клики:", cliques2)
    visualize_graph(G2, cliques2, title="Граф 2")
