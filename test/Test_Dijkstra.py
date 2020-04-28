from Graph import Graph
from DirectedEdge import DirectedEdge
from Dijkstra import Dijkstra, AllPairsDijkstra


def import_distances():
    """Read graph data file from csv to Graph

    :return: A symmetric directed edge-weighted Graph
    """
    with open('data/WGUPS Distance Graph Input.csv', 'r') as file:
        v = file.readline()
        print(v)
        graph = Graph(int(v))
        for line in file.readlines():
            v, w, dist = line.split(',')
            v = int(v)
            w = int(w)
            dist = float(dist)
            edge_one = DirectedEdge(v, w, dist)
            edge_two = DirectedEdge(w, v, dist)
            graph.add_edge(edge_one)
            graph.add_edge(edge_two)
    return graph


def main():
    print("hello world!")

    g = import_distances()
    d = Dijkstra(g, 0)

    t = 4
    if d.ispath(t):
        print(d.dist(t))
        print(d.path(t))


if __name__ == "__main__":
    main()