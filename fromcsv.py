import csv
from Package import Package
from HashDict import HashDict
from Destination import Destination
from Graph import Graph
from DirectedEdge import DirectedEdge


def import_packages():
    """Read Daily Local Deliveries (packages) file from csv to hash table

    :return: 1) hash table dictionary with package id's as keys and Package objects as values
             2) hash table dictionary with location id's as keys and lists of Package objects as values
    """
    packages_pid = HashDict()
    packages_lid = HashDict()
    with open('data/Daily Local Deliveries.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        headers = next(reader, None)
        for row in reader:
            pid, lid, address, city, state, zip_code, deadline, weight, notes = row
            pid = int(pid)
            lid = int(lid)
            weight = float(weight)
            package = Package(pid, lid, address, city, state, zip_code, weight, deadline, 'At hub')
            packages_pid.put(pid, package)
            if packages_lid.get(lid) is None:
                packages_lid.put(lid, [])
            packages_lid.get(lid).append(package)
        if packages_lid.get(0) is None:
            packages_lid.put(0, [])
    return packages_pid, packages_lid


def import_locations():
    """Read locations file from csv to hash table

    :return: hash table dictionary with location id as key and
             (location, address) tuples as values
    """
    locations = HashDict()
    with open('data/WGUPS Destinations Table.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        headers = next(reader, None)
        for row in reader:
            name, address, lid = row
            lid = int(lid)
            destination = Destination(lid, name, address)
            locations.put(lid, destination)
    return locations


def import_distances():
    """Read graph data file from csv to Graph

    :return: A symmetric directed edge-weighted Graph
    """
    with open('data/WGUPS Distance Graph Input.csv', 'r') as file:
        v = file.readline()
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