from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    path = []
    queue = [(0, initial_position)]
    while queue:
        currentCost, currentPos = heappop(queue)
        path.append(currentPos)
        if currentPos == destination:
            return path
        else:
            newCosts = adj(graph, currentPos) #set newCosts equal to the list navigation_edges returns
            for cost in newCosts:
                listPos = cost[0]
                listCost = cost[1]
                if listPos not in path:
                    heappush(queue, (listCost, listPos))
    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    destination_dict = {}
    for point in graph['waypoints']:
        if point is not initial_position:
            path = []
            queue = [(0, initial_position)]
            totalCost = 0
        while queue:
            currentCost, currentPos = heappop(queue)
            totalCost = totalCost + currentCost
            path.append(currentPos)
            if currentPos == graph['waypoints'][point]:
                break
            else:
                newCosts = adj(graph, currentPos)

                for  cost in newCosts:
                    listPos = cost[0]
                    listCost = cost[1]
                    if listPos not in path:
                        heappush(queue, (listCost, listPos))
        destination_dict[point] = totalCost
    return destination_dict

    


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    costs = []
    keyList = level['spaces'].keys()
    initialCost = level['spaces'].get(cell)

    x_coord = cell[0]
    y_coord = cell[1]

    directions = {
        'north':(x_coord, y_coord + 1),
        'east':(x_coord  + 1, y_coord),
        'south':(x_coord, y_coord - 1),
        'west':(x_coord - 1, y_coord),
        'north_east':(x_coord + 1, y_coord + 1),
        'south_east':(x_coord + 1, y_coord - 1),
        'south_west':(x_coord - 1, y_coord - 1),
        'north_west':(x_coord - 1, y_coord + 1)
    }

    specialCases = ['north_east', 'south_east', 'south_west', 'north_west']
    

    for direction in directions:
        if directions[direction] in keyList:
            if direction in specialCases:
                nextCost = level['spaces'].get(directions[direction])
                newCost = ((.5 * sqrt(2)) * initialCost) + ((.5 * sqrt(2)) * nextCost)
                costs.append(direction, newCost)
            else:
                nextCost = level['spaes'].get(directions[direction])
                newCost = (.5 * initialCost) + (.5 * nextCost)
                costs.append(direction, newCost)
    return costs


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
