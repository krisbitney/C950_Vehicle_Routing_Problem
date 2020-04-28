class DirectedEdge:
    """
    A DirectedEdge is a directional edge in a graph, which can optionally be weighted
    """

    def __init__(self, start, end, weight=0):
        self._v = start
        self._w = end
        self._weight = weight

    def start(self):
        """ Returns vertex where edge starts

        :return: vertex v
        """
        return self._v

    def end(self):
        """ Returns vertex where edge ends

        :return: vertex w
        """
        return self._w

    def weight(self):
        """ Returns edge weight

        :return: weight
        """
        return self._weight

    def __repr__(self):
        return ("DirectedEdge(" +
                str(self._v) + ", " +
                str(self._w) + ", " +
                str(self._weight) + ")")

    def __str__(self):
        return str(self._v) + "->" + str(self._w) + " " + str(self._weight)

    def __lt__(self, other):
        return self._weight < other.weight

    def __le__(self, other):
        return self._weight <= other.weight

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return other.__le__(self)

    def __eq__(self, other):
        return self._weight == other.weight

    def __ne__(self, other):
        return not self.__eq__(other)
