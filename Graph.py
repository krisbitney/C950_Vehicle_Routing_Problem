from DirectedEdge import DirectedEdge


class Graph:
    """
    A general graph implementation that accepts directed or undirected edges.
    The graph is implemented as a list of adjacency lists, where each
    adjacency list contains all the edges the start in its associated vertex.
    """

    def __init__(self, V):
        """ Constructor
        Worst case time complexity of O(V)

        :param V: The number of vertexes in the graph
        """
        if not isinstance(V, int) or V < 1:
            raise TypeError("The number of vertexes must be a positive integer")
        self._V = V
        self._E = 0
        self.__adj = [[] for i in range(V)]

    def V(self):
        """ Returns the number of vertexes
        Worst case time complexity of O(1)

        :return: V
        """
        return self._V

    def E(self):
        """ Returns the number of edges
        Worst case time complexity of O(1)

        :return: E
        """
        return self._E

    def add_edge(self, e):
        """ Add an edge to the graph
        Worst case time complexity of O(1)

        :param e: An edge object of type DirectedEdge
        :return:
        """
        if not isinstance(e, DirectedEdge):
            raise TypeError("Only edges of type DirectedEdge are currently supported")
        self.__adj[e.start()].append(e)
        self._E += 1

    def adj(self, v):
        """ Returns all the edges adjacent to vertex v
        Worst case time complexity of O(1)

        :param v: a vertex
        :return: list of edges adjacent to v
        """
        return self.__adj[v]

    def edges(self):
        """ Returns a flattened list of all the edges in the graph
        Worst case time complexity of O(E)

        :return: list of edges
        """
        return [e for v in self.__adj for e in v]
