from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Barcelona_City/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ### BELOW HERE YOU CAN CALL ANY FUNCTION THAT yoU HAVE PROGRAMED TO ANSWER THE QUESTIONS OF THE EXAM ###
    ### this code is just for you, you won't have to upload it after the exam ###

    # Ejemplo 1
    origin = 0
    destination = 0
    for id, values in map.stations.items():
        if values["name"] == "Clot":
            if values["line"] == 4:
                print("found o")
                origin = id
        elif values["name"] == "Bogatell":
            if values["line"] == 3:
                print("found d")
                destination = id

    path = breadth_first_search(origin, destination, map)
    print_list_of_path_with_cost([path])

    # Ejemplo 2
    path = [ 4, 3, 2, 1, 7, 8]          # starts with 5
    newPath = Path(5)
    for node in path:
        newPath.add_route(node)
        calculate_cost([newPath], map, 2)    # 2 for distance

    print(newPath.g)


    #this is an example of how to call some of the functions that you have programed
    example_path=uniform_cost_search(9, 3, map, 1)
    print_list_of_path_with_cost([example_path])

