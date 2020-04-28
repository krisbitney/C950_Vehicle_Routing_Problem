from Dijkstra import AllPairsDijkstra


class NNRoutePlanner:
    """
    Given a Graph, this class implements nearest-neighbor optimization functions that take
    a set of location id's (e.g., a list) and find a low-mileage order in which to drive
    to each location. The classes uses Dijkstra's shortest paths algorithm to determine the
    distances between locations. It uses a greedy approach wherein at each step it chooses
    the next closest location not visited in previous steps.

    The worst case time complexity of the algorithm is O(VElogV). Here, V is the number of vertices (locations)
    in the underlying graph and E is the number of edges in the graph.

    The space complexity is proportional to V+E.
    """

    def __init__(self, graph):
        # find shortest paths -> O(VElogV)
        self.short_paths = AllPairsDijkstra(graph)

    def optimize_route(self, locations):
        """ Arrange list of locations into optimized path.
        The worst case time complexity is O(NN), where N is
        the number of delivery stops in the route.

        :param locations: iterable of location id's
        :return: optimized path (as an ordered list)
        """
        path = [0]
        for i in range(len(locations)):
            nn = 0
            minimum = float('inf')
            for j in locations:
                if j in path:
                    continue
                dist = self.short_paths.dist(path[i], j)
                if dist < minimum:
                    minimum = dist
                    nn = j
            if nn in path:
                continue
            path.append(nn)
        path.append(0)
        return path

    def optimize_plan(self, plan):
        """ Arrange each list of locations into optimized paths.
        This is a convenience function that runs the
        optimize_route() function on each element in the argument.
        The worst case time complexity is O(NN), where N is the
        number of delivery stops in the route plan.

        :param plan: list of iterables containing location id's
        :return: list of optimized paths (as ordered lists)
        """
        optimized = []
        for route in plan:
            optimized.append(self.optimize_route(route))
        return optimized

    def score_all(self, plan):
        """ Given a list of paths (ordered list of locaiton id's), determines
        the miles required to complete the paths based on shortest-paths
        distances between locations.
        The worst case time complexity is O(N) where N is the number of
        delivery stops in the route plan

        :param plan: list of lists of locaiton id's
        :return: total of path costs (in miles)
        """
        cost = 0
        for i in range(len(plan)):
            for j in range(len(plan[i]) - 1):
                cost += self.short_paths.dist(plan[i][j], plan[i][j + 1])
        return cost

    def score_route(self, route):
        """ Given a path (ordered list of locaiton id's), determines
        the miles required to complete the path based on
        shortest-paths distances between locations.
        Worst case time complexity is O(N) where N is the
        number of delivery stops in the route.

        :param route: list of location id's
        :return: path cost (in miles)
        """
        cost = 0
        for i in range(len(route) - 1):
            cost += self.short_paths.dist(route[i], route[i + 1])
        return cost

    def distances(self, plan):
        """ Given a list of paths (ordered lists of location id's), returns
        a 2d array (list of lists) with elements representing locations'
        distances from the prior location in its path. Each element in the
        distances array corresponds to a location in the given list of paths.
        The worst case time complexity is O(N) where N is the number of
        delivery stops in the route plan.

        :param plan: list of lists of location id's
        :return: list of lists of distances from prior elements in paths
        """
        distances = []
        for i in range(len(plan)):
            distances.append([0])
            for j in range(len(plan[i]) - 1):
                distances[i].append(self.short_paths.dist(plan[i][j], plan[i][j + 1]))
        return distances

    def calculate_loads(self, plan, packages):
        """ calculates the number of packages on each vehicle/route.
        The worst case time complexity is O(N) where N is the number of delivery
        stops in the route plan.

        :param plan: list of lists of location id's
        :param packages: dictionary where keys are location id's and values are Package objects
        :return:
        """
        loads = [0 for i in range(len(plan))]
        for i in range(len(plan)):
            for loc_id in plan[i]:
                loads[i] += len(packages.get(loc_id))

    def path(self, s, t):
        """ Returns shortest path from vertex s to vertex t
        Worst case time complexity of O(V)

        :param s: source vertex
        :param t: target vertex
        :return: list of vertices in order of path from vertex s to vertex t
        """
        return self.short_paths.path(s, t)

