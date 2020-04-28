
class Routes:
    """
    Holds data on routes, including constraints, and provides functions to simulate route status at specified times
    The main data structure is a "route plan", which is a list of routes, where a route is a list of location id's.

    This class also keeps track of packages associated with the route plan, the number of packages on each route,
    the total cost (in miles) of the route plan, and the distances between delivery locations.

    This class can be used with the Route Planner algorithms. The class was created to keep the data structures
    and algorithms decoupled as much as possible.
    """

    def __init__(self, packages, n_routes=0, capacity=16):
        """ Constructor
        Worst case time complexity of O(1)

        """
        self.packages = packages
        self.capacity = capacity
        # number of routes
        if n_routes == 0:
            num_packages = 0
            for packages in self.packages.values():
                num_packages += len(packages)
            n_routes = 1 + (num_packages // capacity)
        self.n_routes = n_routes
        # initialize route plan
        self.plan = None
        self.loads = None
        self.cost = None
        self.distances = None
        # initialize constraints lists
        self.constraints = [set() for i in range(n_routes)]
        # time/speed for package statuses -> this is for demonstration purposes
        self.departure_times = [0, 0, 0, 0]
        self.time_since_eight = 0
        self.mph = 18

    def get(self, route):
        """ Returns route array, given route number

        :param route: index of route in route plan
        :return:
        """
        return self.plan[route]

    def constrain(self, route, v):
        """ Constrain a vertex (location id) to remain in a route

        :param route: index of route in route plan
        :param v: location id
        :return:
        """
        self.constraints[route].add(v)

    def lift(self, route, v):
        """ Remove restriction on vertex in route

        :param route: index of route in route plan
        :param v: location id
        :return:
        """
        if v in self.constraints[route]:
            self.constraints[route].remove(v)

    def set_departure_time(self, route, hours_since_8am):
        """ Set departure time for route, specified in number of hours since 8:00am

        :param route: index of route in route plan
        :param hours_since_8am: number of hours since 8:00am
        :return:
        """
        self.departure_times[route] = hours_since_8am

    def set_time(self, hours_since_8am):
        """ Updates statuses of packages to simulate their projected status at a given time

        :param hours_since_8am: number of hours since 8:00am
        :return:
        """
        progress = []
        for i in range(self.n_routes):
            progress.append(self.mph * (hours_since_8am - self.departure_times[i]))
            dist = 0
            for j in range(len(self.plan[i])):
                dist += self.distances[i][j]
                for package in self.packages.get(self.plan[i][j]):
                    if package.pid == 9 and i == 1 or \
                       package.pid == 5 and i == 3 or \
                       package.pid == 37 and i == 3 or \
                       package.pid == 38 and i == 3:
                        continue
                    if progress[i] < 0:
                        package.status = 'At hub'
                    elif progress[i] >= dist:
                        package.status = 'Delivered'
                    else:
                        package.status = 'In route'







