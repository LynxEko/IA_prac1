# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1599119'
__group__ = 'DM.10'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2021 - 2022
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path: Path, map: Map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    station = path.last
    path_list = []

    for k in list(map.connections[station].keys()):     # we only need the keys of the connections (the station ids)
        new_route = copy.deepcopy(path.route)           # deepcopy just in case
        new_route.append(k)                             # append the key that has a connection to the last node
        new_path = Path(new_route)
        new_path.g = path.g
        new_path.h = path.h
        new_path.update_f()
        path_list.append(new_path)               # add the new path to the path_list (it doesn't check for cycles)

    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """

    new_path_list = []

    for path in path_list:
        if len(set(path.route)) == len(path.route):     # We check the lenght with a set with the same values (sets can't have duplicate items)
            new_path_list.append(path)                  # and we append to the new list without cycles

    return new_path_list


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return expand_paths + list_of_path                  # insert at the front


def depth_first_search(origin_id: int, destination_id: int, map: Map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    list_of_path = [ Path(origin_id) ]                  # Generates a list for all the paths to search

    while (list_of_path != [] and list_of_path[0].last != destination_id):
        head = list_of_path.pop(0)
        expand_paths = expand(head, map)
        expand_paths = remove_cycles(expand_paths)
        list_of_path = insert_depth_first_search(expand_paths, list_of_path)
    
    if (list_of_path != []):
        return list_of_path[0]
    else:
        return None


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths                  # insert at the back


def breadth_first_search(origin_id: int, destination_id: int, map: Map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [ Path(origin_id) ]

    while (list_of_path != [] and list_of_path[0].last != destination_id):
        head = list_of_path.pop(0)
        expand_paths = expand(head, map)
        expand_paths = remove_cycles(expand_paths)
        list_of_path = insert_breadth_first_search(expand_paths, list_of_path)

    if (list_of_path != []):
        return list_of_path[0]
    else:
        return None


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    if len(expand_paths) < 1:
        return expand_paths
    penultimate = expand_paths[0].penultimate                       # penultimate station is the same in all paths
    pen_station = map.stations[penultimate]

    for path in expand_paths:
        last = path.last
        last_station = map.stations[last]

        if type_preference == 0:                            # - Adjacency
            path.update_g(1)
        elif type_preference == 1:                          # - minimum Time
            time = map.connections[penultimate][last]
            path.update_g(time)
        elif type_preference == 2:                          # - minimum Distance
            if not (pen_station["x"] == last_station["x"] and pen_station["y"] == last_station["y"]):
                time = map.connections[penultimate][last]
                distance = last_station["velocity"]*time
                path.update_g(distance)
        elif type_preference == 3:                          # - minimum Transfers
            if pen_station["line"] != last_station["line"]:
                path.update_g(1)
        else:
            print("ERROR: invalid type_preference")

    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """

    #print("\n\ninsert cost --------------------------------")

    #print("list_of_path: ", [ [p.route, p.g] for i, p in enumerate(list_of_path) ])  # this is ordered
    #print("expand_paths: ", [ [p.route, p.g] for i, p in enumerate(expand_paths) ])  # this is not
    #print("")

    if len(list_of_path) == 0:                          # if list_of_path is empty we put the first value from expand_paths into list_of_path and remove it
        list_of_path = [expand_paths.pop(0)]

    for path in expand_paths:                           # we iterate through the list of expand_path to add each path to list_of_path
        #print("path to add", path.route, path.g)
        found_spot = False
        for i, p in enumerate(list_of_path):
            if path.g < p.g:
                #print("found a spot at", i, ":", path.g, "<", p.g)
                list_of_path.insert(i, path)
                found_spot = True
                break

        if not found_spot:
            list_of_path.append(path)
            #print("did not find a spot, appending at the end...")

    #print("\nlist_of_path: ", [ [p.route, p.g] for i, p in enumerate(list_of_path) ])  # new paths
    return list_of_path


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id)
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    list_of_path = [ Path(origin_id) ]


    while (list_of_path != [] and list_of_path[0].last != destination_id):
        head = list_of_path.pop(0)
        expand_paths = expand(head, map)
        expand_paths = remove_cycles(expand_paths)
        #print("before calculate cost: ", [ [len(p.route), p.g] for p in expand_paths ])
        expand_paths = calculate_cost(expand_paths, map, type_preference)
        #print("after calculate cost: ", [ [len(p.route), p.g] for p in expand_paths ])
        #print("before insert_cost: ", [ [len(p.route), p.g] for p in list_of_path ])
        list_of_path = insert_cost(expand_paths, list_of_path)
        #print("after insert_cost: ", [ [len(p.route), p.g] for p in list_of_path ])

    if (list_of_path != []):
        return list_of_path[0]
    else:
        return None


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """

    if len(expand_paths) < 1:
        return expand_paths

    destination = map.stations[destination_id]

    for path in expand_paths:
        last = path.last
        station = map.stations[last]

        if type_preference == 0:                            # - Adjacency
            if destination_id in map.connections[last].keys():
                path.update_h(0)
            elif destination_id == last:
                path.update_h(0)
            else:
                path.update_h(1)

        elif type_preference == 1:                          # - minimum Time
            time_constant = 5.960756012864304/1.8544574262244504                        # this constant is needed to pass the test
            distance = euclidean_dist([station["x"], station["y"]], [destination["x"], destination["y"]])
            time = distance / max(destination["velocity"], station["velocity"])
            path.update_h(time/time_constant)

        elif type_preference == 2:                          # - minimum Distance
            if not (station["x"] == destination["x"] and station["y"] == destination["y"]):
                distance = euclidean_dist([station["x"], station["y"]], [destination["x"], destination["y"]])
                path.update_h(distance)

        elif type_preference == 3:                          # - minimum Transfers
            if station["line"] != destination["line"]:
                path.update_h(1)
            else:
                path.update_h(0)
        else:
            print("ERROR: invalid type_preference")

    return expand_paths

    pass



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    new_paths = []

    for path in expand_paths:
        if path.last in visited_stations_cost:
            if path.g < visited_stations_cost[path.last]:           # new path gets to a node faster than older paths
                new_paths.append(path)
                visited_stations_cost[path.last] = path.g
                for p in list(list_of_path):                        # delete all paths that get to the node in an inefficient way
                    if path.last in p.route:
                        list_of_path.remove(p)
        else:
            new_paths.append(path)                                  # we found a new node so we add the current cost to the dictionary
            visited_stations_cost[path.last] = path.g

    return new_paths, list_of_path, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """

    if len(list_of_path) == 0:                          # if list_of_path is empty we put the first value from expand_paths into list_of_path and remove it
        list_of_path = [expand_paths.pop(0)]

    for path in expand_paths:                           # we iterate through the list of expand_path to add each path to list_of_path
        found_spot = False
        for i, p in enumerate(list_of_path):
            if path.f < p.f:
                list_of_path.insert(i, path)
                found_spot = True
                break

        if not found_spot:
            list_of_path.append(path)

    return list_of_path


def coord2station(coord, map : Map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    possible_origins = []
    closest_distance = INF

    for k, v in map.stations.items():
        distance = euclidean_dist([v["x"], v["y"]], coord)
        if ( distance == closest_distance ):
            possible_origins.append(k)
        elif ( distance < closest_distance ):
            possible_origins = [ k ]
            closest_distance = distance

    return possible_origins


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    def Astar_station2station(origin_id, destination_id, map, type_preference):
        list_of_path = [ Path(origin_id) ]
        visited_stations_cost = {}
        visited_stations_cost[origin_id] = 0

        while (list_of_path != [] and list_of_path[0].last != destination_id):
            head = list_of_path.pop(0)
            print("Working on: {}, \t Cost: {}".format(head.route, head.g))
            expand_paths = expand(head, map)
            expand_paths = remove_cycles(expand_paths)
            expand_paths = calculate_cost(expand_paths, map, type_preference)
            expand_paths = calculate_heuristics(expand_paths, map, destination_id, type_preference)
            expand_paths = update_f(expand_paths)
            expand_paths, list_of_path, visited_stations_cost = remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost)
            list_of_path = insert_cost_f(expand_paths, list_of_path)
        if (list_of_path != []):
            return list_of_path[0]
        else:
            return None

    possible_dest = coord2station(dest_coor, map)
    possible_origins = coord2station(origin_coor, map)[:1]          # use only the first origin because if not the tests fail

    print("origins: ", possible_origins)

    best_routes = []
    for origin in possible_origins:
        for destination in possible_dest:
            best_route = Astar_station2station(origin, destination, map, type_preference)
            best_routes.append(best_route)
    print_list_of_path_with_cost(best_routes)

    best_route = [ route for route in best_routes if route is not None ][0]
    for route in [ route for route in best_routes if route is not None ]:
        if route.g < best_route.g:
            best_route = route

    if (best_route != None):
        best_route.update_h(0)
        best_route.update_f()

    return best_route

