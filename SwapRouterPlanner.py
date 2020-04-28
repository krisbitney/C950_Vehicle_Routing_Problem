from Dijkstra import AllPairsDijkstra

import random


class SwapRoutePlanner:
    """
    Given a Routes object, which contains data on packages and routes, this class implements
    an algorithm that determines the optimal location distribution (i.e., which packages should
    go on which routes) and minimizes the total miles required for the combined routes.

    The algorithm finds good routes by searching for marginal improvements in a route plan until a local
    optimum is reached. It determines whether an improvement is really an improvement by comparing changes in
    total miles based on Dijkstra's shortest paths algorithm. The class repeats the local optimization process
    multiple times, randomly shuffling the initial starting conditions between each repeat. In doing so, it
    increases the likelihood of finding a global optimum.

    The time complexity of the algorithm is VElogV + R(V + 2CV^2 I), with worst case
    time complexity proportional to O(VElogV). Here, V is the number of vertices (locations) in the underlying
    graph, E is the number of edges in the graph, R is the number of restarts used to search for a global
    optimum, C is vehicle capacity, and I is the number of iterations used to converge to a local optimum.

    The space complexity is proportional to VV+V, which is required for the graph data structure on which
    Dijkstra's algorithm is based.
    """

    def __init__(self, graph, routes):
        self.graph = graph
        self.routes = routes
        # find shortest paths
        self.short_paths = AllPairsDijkstra(self.graph)
        # initialize route plan
        self.plan, self.loads = self._initialize()
        # find initial route costs (in miles)
        self.cost = self.score_all(self.plan)

    def optimize_global(self, starts=3, iterations=20, early_stopping=2, tol=1, verbose=0):
        """ Repeatedly shuffles route plan and runs optimize_local() function in order to increase the likelihood
        that a global optimum is found.
        Worst case time complexity is O(R(V + 2CIVV) where R is the number of restarts/repeats, V is the number
        of delivery addresses in the route plan, C is vehicle capacity, and I is the number of iterations required to
        converge to local optima in the optimize_local() algorithm.

        :param starts: Number of restarts/repeats of the shuffle + optimize_local() function
        :param iterations: Number of iterations for each optimize_local() run
        :param early_stopping: stop early if this many subsequent iterations does not lead to improvement
        :param tol: definition of "no improvement" used in early stopping, where improvements less than tol are ignored
        :param verbose: 0, 1, or 2 indicates the amount of detail to print to console while the algorithm operates
        :return:
        """
        print(f"Start cost: {self.cost}")
        plan = self.plan
        loads = self.loads
        cost = self.cost
        for start in range(starts):
            self.shuffle(plan, loads, 2)
            cost = self._optimize_local(plan, loads, cost, start,
                                        iterations=iterations,
                                        early_stopping=early_stopping,
                                        tol=tol,
                                        verbose=verbose)
            if cost < self.cost:
                self.plan = [list(route) for route in plan]
                self.loads = list(loads)
                self.cost = cost
                if verbose > 0:
                    print(f"New minimum cost: {self.cost}")
        self.clean_plan(self.plan)
        self.cost = self.score_all(self.plan)
        print(f"End cost: {self.cost}")
        return self.plan, self.loads, self.cost

    def _optimize_local(self, plan, loads, cost, start=1, iterations=15, early_stopping=2, tol=1, verbose=0):
        """ Swap locations between and within routes until convergence to a local optimum. This function changes
        the given data in place.
        Worst case time complexity is O(2CIVV) where C is vehicle capacity, I is the number of iterations to run,
        and V is the number of locations in the route plan.

        :param plan: route plan
        :param loads: list of route loads (number of packages in each route)
        :param cost: starting total mileage required to complete route
        :param start: integer used to track how many times the optimize_local() function has been repeated
        :param iterations: number of times to iterate the optimize_local() algorithm in each function run
        :param early_stopping: stop early if this many subsequent iterations does not lead to improvement
        :param tol: definition of "no improvement" used in early stopping, where improvements less than tol are ignored
        :param verbose: 0, 1, or 2 indicates the amount of detail to print to console while the algorithm operates
        :return: cost of best route
        """
        last_cost = cost
        no_change_count = 0
        if verbose > 1:
            print(f"\tStarting cost in start {start}: {self.cost}")
        for iteration in range(iterations):
            for i in range(len(plan)):
                for j in range(1, len(plan[i]) - 1):
                    for ai in range(i, len(plan)):
                        for aj in range(j, len(plan[ai]) - 1):
                            # validate constraints
                            if not self._validate_constraints(plan, i, ai, j, aj):
                                continue
                            # validate capacities
                            valid_cap, new_i_cap, new_ai_cap = self._validate_capacities(plan, loads, i, ai, j, aj)
                            if valid_cap:
                                current_cost = self.score_route(plan[i]) + self.score_route(plan[ai])
                                self.swap(plan, i, ai, j, aj)
                                alt_cost = self.score_route(plan[i]) + self.score_route(plan[ai])
                                # swap if improvement
                                if alt_cost <= current_cost:
                                    loads[i] = new_i_cap
                                    loads[ai] = new_ai_cap
                                else:
                                    self.swap(plan, i, ai, j, aj)
            # update cost
            new_cost = self.score_all(plan)
            if new_cost < cost:
                cost = new_cost
                if verbose > 1:
                    print(f"\tNew minimum cost in start {start} on iteration {iteration}: {new_cost}")
            # early stopping
            if abs(last_cost - new_cost) < tol:
                no_change_count += 1
                if no_change_count == early_stopping:
                    break
            else:
                no_change_count = 0
            last_cost = new_cost
        return cost

    def shuffle(self, plan, loads, repetitions=1):
        """ Shuffle plan in-place while obeying constraints
        Worst case time complexity is O(N) where N is the number
        of delivery addresses

        :param plan: route plan
        :param loads: list of route loads (number of packages in a route)
        :param repetitions: number of times to repeat shuffle
        :return:
        """
        capacity = self.routes.capacity
        n_routes = self.routes.n_routes
        constraints = self.routes.constraints
        for repeat in range(repetitions):
            for i in range(n_routes):
                for j in range(1, capacity - 1):
                    # constrained packages must stay on same vehicle
                    if plan[i][j] in constraints[i]:
                        alt_i = i
                        alt_j = random.randint(j, capacity - 2)
                    # otherwise random swap
                    else:
                        alt_i = random.randint(i, n_routes - 1)
                        alt_j = random.randint(j, capacity - 2)
                    # skip if constraint violated
                    if not self._validate_constraints(plan, i, alt_i, j, alt_j):
                        continue
                    # swap if not over capacity
                    valid_cap, new_i_cap, new_alt_i_cap = self._validate_capacities(plan, loads, i, alt_i, j, alt_j)
                    if valid_cap:
                        self.swap(plan, i, alt_i, j, alt_j)
                        loads[i] = new_i_cap
                        loads[alt_i] = new_alt_i_cap

    def _initialize(self):
        """ Initializes route plan based on set of packages and requirements.
        Worst case time complexity is O(NR) where N is the number of locations
        and R is the number of routes.

        :return: route plan, list of route loads
        """
        packages = self.routes.packages
        capacity = self.routes.capacity
        n_routes = self.routes.n_routes
        constraints = self.routes.constraints
        plan = [[0] for i in range(n_routes)]
        loads = [0 for i in range(n_routes)]
        for loc_id in packages.keys():
            # first enforce constraints
            placed = False
            for i in range(n_routes):
                if loc_id in constraints[i]:
                    loads[i] += len(packages.get(loc_id))
                    plan[i].append(loc_id)
                    placed = True
                    break
            if placed:
                continue
            # otherwise assign to shortest route
            shortest = 0
            minimum = loads[0]
            for i in range(n_routes):
                if loads[i] < minimum:
                    shortest = i
                    minimum = loads[i]
            loads[shortest] += len(packages.get(loc_id))
            plan[shortest].append(loc_id)
        # fill empty slots with zeros to represent hub (keeps lists at length 16)
        for route in plan:
            while len(route) < capacity:
                route.append(0)
        return plan, loads

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

    def swap(self, plan, i, alt_i, j, alt_j):
        """ exchange two items between two arrays
        Worst case time complexity is O(1)

        :param plan: route plan
        :param i: route index for first route
        :param alt_i: route index for second route
        :param j: index of location id in first route list
        :param alt_j: index of location id in second route list
        :return:
        """
        temp = plan[i][j]
        plan[i][j] = plan[alt_i][alt_j]
        plan[alt_i][alt_j] = temp

    def _validate_constraints(self, plan, i, alt_i, j, alt_j):
        """ Make sure potential swap does not violate constraints
        requiring that packages remain on specific vehicles.
        Worst case time complexity is O(1)

        :param plan: route plan
        :param i: route index for first route
        :param alt_i: route index for second route
        :param j: index of location id in first route list
        :param alt_j: index of location id in second route list
        :return: boolean confirming or rejecting swap validity
        """
        constraints = self.routes.constraints
        if i != alt_i and (plan[i][j] in constraints[i] or plan[alt_i][alt_j] in constraints[alt_i]):
            return False
        return True

    def _validate_capacities(self, plan, loads, i, alt_i, j, alt_j):
        """ Make sure a potential swap does not violate capacity maximums.
        Worst case time complexity is O(1)

        :param plan: route plan
        :param loads: current vehicle loads
        :param i: route index for first route
        :param alt_i: route index for second route
        :param j: index of location id in first route list
        :param alt_j: index of location id in second route list
        :return: boolean confirming or rejecting swap validity, first route new capacity, second route new capacity
        """
        if i == alt_i:
            return True, loads[i], loads[i]
        packages = self.routes.packages
        capacity = self.routes.capacity
        n_pack_ij = len(packages.get(plan[i][j]))
        n_pack_alt_ij = len(packages.get(plan[alt_i][alt_j]))
        i_new_capacity = loads[i] - n_pack_ij + n_pack_alt_ij
        alt_i_new_capacity = loads[alt_i] + n_pack_ij - n_pack_alt_ij
        if i_new_capacity > capacity or alt_i_new_capacity > capacity:
            return False, loads[i], loads[alt_i]
        return True, i_new_capacity, alt_i_new_capacity

    def clean_plan(self, plan):
        """ Remove excess zeros from Route plan
        Worst case time complexity is O(NN) where N is the
        number of delivery stops in the route plan

        :param plan:
        :return:
        """
        for route in plan:
            while 0 in route:
                route.remove(0)
            route.insert(0, 0)
            route.append(0)

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
