from IndexMinPQ import IndexMinPQ
from Graph import Graph


class Dijkstra:
    """
    Implementation of Dijkstra's classic shortest path algorithm. This implementation
    finds shortest path from a source vertex to every vertex reachable from the source.
    It is based on the implementation described in Algorithms 4e (Sedgewick & Wayne, 2011).

    Where V is the number of vertices and E the number of edges in the graph:
    Constructor runs algorithm with worst case time complexity of O(E*logV)
    Uses extra space proportional to V
    """

    def __init__(self, graph, source):
        """ Constructor
        Worst case time complexity of O(E*logV)

        :param graph: a graph of type Graph
        :param source: source vertex from which paths are discovered
        """
        if not isinstance(graph, Graph):
            raise TypeError("only Graph objects are currently supported")
        if not isinstance(source, int):
            raise TypeError("source vertex must be an integer")
        # instantiate data structures
        self.__edgeto = [None] * graph.V()
        self.__distto = [float('inf')] * graph.V()
        self.__distto[source] = 0
        self.__pq = IndexMinPQ(graph.V())
        # run algorithm
        self.__pq.insert(source, 0)
        while not self.__pq.empty():
            self.__relax(graph, self.__pq.del_min())

    def __relax(self, graph, v):
        for edge in graph.adj(v):
            w = edge.end()
            if self.__distto[w] > self.__distto[v] + edge.weight():
                self.__distto[w] = self.__distto[v] + edge.weight()
                self.__edgeto[w] = edge
                if self.__pq.contains(w):
                    self.__pq.change_key(w, self.__distto[w])
                else:
                    self.__pq.insert(w, self.__distto[w])

    def dist(self, v):
        """ Returns shortest path distance from source vertex to vertex v,
        or float('inf') if no path exists.
        Worst case time complexity of O(1)

        :param v: target vertex
        :return: distance from source to v
        """
        return self.__distto[v]

    def ispath(self, v):
        """ Test if path exists from source vertex to vertex v
        Worst case time complexity of O(1)

        :param v: target vertex
        :return: True if path exists, False otherwise
        """
        return self.__distto[v] < float('inf')

    def path(self, v):
        """ Returns shortest path from source vertex to vertex v
        Worst case time complexity of O(V)

        :param v: target vertex
        :return: list of vertices in order of path from source to v
        """
        if not self.ispath(v):
            return None
        path = []
        edge = self.__edgeto[v]
        while edge is not None:
            path.append(edge)
            edge = self.__edgeto[edge.start()]
        path.reverse()
        return path


class AllPairsDijkstra:
    """ Implements Dijkstra's classic shortest paths algorithm for all pairs of vertices in a graph

    Where V is the number of vertices and E the number of edges in the graph:
    Constructor runs algorithm with worst case time complexity of O(V*E*logV))
    Uses extra space proportional to V^2
    """

    def __init__(self, graph):
        """ Constructor
        Worst case time complexity of O(V*E*logV)

        :param graph: a graph of type Graph
        """
        if not isinstance(graph, Graph):
            raise TypeError("only Graph objects are currently supported")
        self.__paths = [Dijkstra(graph, s) for s in range(graph.V())]

    def dist(self, s, t):
        """ Returns shortest path distance from vertex s to vertex t,
        or float('inf') if no path exists.
        Worst case time complexity of O(1)

        :param s: source vertex
        :param t: target vertex
        :return: distance from s to t
        """
        if s == t:
            return 0
        return self.__paths[s].dist(t)

    def ispath(self, s, t):
        """ Test if path exists from vertex s to vertex t
        Worst case time complexity of O(1)

        :param s: source vertex
        :param t: target vertex
        :return: True if path exists, False otherwise
        """
        return self.__paths[s].ispath(t)

    def path(self, s, t):
        """ Returns shortest path from vertex s to vertex t
        Worst case time complexity of O(V)

        :param s: source vertex
        :param t: target vertex
        :return: list of vertices in order of path from vertex s to vertex t
        """
        return self.__paths[s].path(t)


