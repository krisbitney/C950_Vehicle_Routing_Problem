def print_status(packages_pid, package_id):
    """ Print status of specific package

    :param packages_pid: package dictionary where keys are package ids
    :param package_id: package id
    :return:
    """
    print(f"Package: {package_id} Deadline: {packages_pid.get(package_id).deadline} Status: {packages_pid.get(package_id).status}")


def print_all_statuses(packages_pid):
    """ Print status of all packages in dictionary

    :param packages_pid: package dictionary where keys are package ids
    :return:
    """
    for pid, package in packages_pid:
        print(f"Package: {pid} Deadline: {package.deadline} Status: {package.status}")


def print_route_status(packages_lid, route):
    """ Print status of all packages in route

    :param packages_lid: package dictionary where keys are location ids
    :param route: iterable of location ids
    :return:
    """
    print(f"Rotue: {route}")
    for lid in route:
        for package in packages_lid.get(lid):
            print(f"Package: {package.pid} Deadline: {package.deadline} Status: {package.status}")