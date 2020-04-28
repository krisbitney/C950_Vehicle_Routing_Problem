import fromcsv
import reporting
from NNRoutePlanner import NNRoutePlanner
from SwapRouterPlanner import SwapRoutePlanner
from Routes import Routes


def main():
    graph = fromcsv.import_distances()
    packages_pid, packages_lid = fromcsv.import_packages()

    # prepare route parameters
    routes = Routes(packages_lid, n_routes=4, capacity=16)
    # Can only be on truck 2
    routes.constrain(1, 4)
    routes.constrain(1, 12)
    routes.constrain(1, 20)
    routes.constrain(1, 21)
    # must be delivered together
    routes.constrain(0, 2)
    routes.constrain(0, 5)
    routes.constrain(0, 6)
    # arrives at 9:05 am
    routes.constrain(2, 9) # 10:30am deadline
    routes.constrain(2, 25) # 10:30am deadline
    routes.constrain(2, 16)
    routes.constrain(2, 15)
    # arrives at 10:20 am
    # routes.constrain(3, 21)

    # optimize routes
    planner = SwapRoutePlanner(graph, routes)
    routes.plan, routes.loads, routes.cost = planner.optimize_global(starts=100, verbose=1)
    # manually load the delayed package and recalculate mileage
    routes.plan[3].append(21)
    planner.clean_plan(routes.plan)
    routes.cost = planner.score_all(routes.plan)
    routes.loads = planner.calculate_loads(routes.plan, packages_lid)
    # calculate distances between route stops (these are shortest paths)
    routes.distances = planner.distances(routes.plan)
    # view cost
    print()
    print(f"Final mileage: {routes.cost}")
    print("Final plan (by route and location id):")
    print(routes.plan)

    # set departure time for status checking
    routes.set_departure_time(0, 0)
    routes.set_departure_time(1, 0)
    routes.set_departure_time(2, 1+5/60)
    routes.set_departure_time(3, 2+20/60)

    # get SP version
    sp_routes = Routes(packages_lid, n_routes=4, capacity=16)
    sp_plan = [[0, 1, 6, 2, 5, 0],
               [0, 18, 10, 3, 12, 21, 13, 4, 20, 23, 19, 0],
               [0, 15, 14, 9, 7, 17, 16, 22, 11, 24, 8, 25, 26, 0],
               [0, 21, 0]]
    nn_planner = NNRoutePlanner(graph)
    sp_routes.plan = nn_planner.optimize_plan(sp_plan)
    sp_routes.cost = nn_planner.score_all(sp_routes.plan)
    sp_routes.distances = nn_planner.distances(sp_routes.plan)
    print()
    print(f"Final mileage: {sp_routes.cost}")
    print("Final plan (by route and location id):")
    print(sp_routes.plan)

    # set departure time for status checking
    # sp_routes.set_departure_time(0, 0)
    # sp_routes.set_departure_time(1, 0)
    # sp_routes.set_departure_time(2, 1+5/60)
    # sp_routes.set_departure_time(3, 2+20/60)

    # set time of day to 9:00am and view statuses
    print()
    print("Time is 9:00am")
    routes.set_time(1)
    reporting.print_all_statuses(packages_pid)
    # set time of day to 10:25am and view statuses
    print()
    print("Time is 10:25am")
    routes.set_time(2+25/60)
    reporting.print_all_statuses(packages_pid)
    # set time of day to 1:00pm and view statuses
    print()
    print("Time is 1:00pm")
    routes.set_time(5)
    reporting.print_all_statuses(packages_pid)


if __name__ == "__main__":
    main()
