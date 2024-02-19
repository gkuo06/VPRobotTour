import networkx as nx
import matplotlib.pyplot as plt
import math

def create_grid_graph(size, edge=None, checkpoints=None):
    G = nx.grid_2d_graph(size, size)

    # Add the part about checkpoints to this and make the conditional a compound conditional
    if edge is not None:
        for coordinate in edge:
            G.remove_edge(coordinate[0][0], coordinate[0][1])

    return G

def draw_grid(G, path=None):
    pos = {(x, y): (y, -x) for x, y in G.nodes()}

    color_map = []
    for node in G.nodes():
        x, y = node
        if (x + y) % 2 == 0:
            color_map.append('orange')  # Replace 'color1' with ORANGE
        else:
            color_map.append("lightblue")  # Replace 'color2' with LIGHT BLUE

    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=600)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green")
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="green", width=2)

    plt.show()

# The point is that path contains a list of tuples that represent the coordinates of the path it takes
# False will represent the y-axis, True will represent the x-axis
def calc_turns(path, num_turn=0):
    axis = path[0][1] == path[1][1]

    for i in range(1,len(path)-1):
        temp = path[i][1] == path[i+1][1]
        if temp is not  axis:
            num_turn += 1
            axis = temp
            print(f"FOUND TURN AT ({path[i][0]}, {path[i][1]})")
        print(f"Coordinates of node {i}: {path[i]}")
    print(f"Moved: {len(path)-1}")
    print(f"Turned: {num_turn}\n")

# Uses distance formula to compute how far two coordinates are from each other
def find_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Maybe use optimization to determine which gateways to shoot for? Probably should eliminate one gateway at least...
# Idea is to find the coordinate of the node in each checkpoint that is closest to the most optimal path.
# COMPLETED TESTING 12/20/23: NEED TO OPTIMIZE DISTANCE FORMULA, CHECK DISCORD FOR SCREENSHOT
# DISTANCE FORMULA HAS BEEN OPTIMIZED, NOW CHECKS FOR DISTANCE IT NEEDS TO TRAVEL AS OPPOSED TO HOW CROW FLIES.

def calc_weight(G, start, end, edge, checkpoints, turns=None, turn_time=4, travel_time=1):
    path = nx.shortest_path(G, source=start, target=end, method='dijkstra')

    nearest_checkpoint_coords = []

    # Should in theory add all the nearest checkpoint coords to the list
    for checkpoint in checkpoints:
        min_distance = float("inf")
        min_distance_coordinate = checkpoint
        for coord2 in path:
            distance = len(nx.shortest_path(G, source=checkpoint, target=coord2, method='dijkstra'))
            if distance < min_distance:
                min_distance = distance
                min_distance_coordinate = checkpoint
        nearest_checkpoint_coords.append(min_distance_coordinate)

    nearest_checkpoint_coords = sorted(nearest_checkpoint_coords, key=lambda coord: find_distance(coord, start))
    print(f"Nearest coords: {nearest_checkpoint_coords}")

    return nearest_checkpoint_coords


def createGrid(start=(0,0), end=(3,3), edge=None, checkpoints=None):
    # Initialize the graph
    G = create_grid_graph(4, edge, checkpoints)

    # Split the path into many parts and then join together using list "full_path"
    if edge is not None and checkpoints is not None:
        waypoints = calc_weight(G, start, end, edge, checkpoints)

        full_path = []
        path_directions = ["forward"]

        full_path.extend(nx.shortest_path(G, source=start, target=waypoints[0], method="dijkstra")[:-1])

        for i in range(len(waypoints) - 1):
            segment_start = waypoints[i]
            segment_end = waypoints[i + 1]
            path_segment = nx.shortest_path(G, source=segment_start, target=segment_end, method="dijkstra")

            if i < len(waypoints) - 2:
                full_path.extend(path_segment[:-1])  # Exclude last node of segment
            else:
                full_path.extend(path_segment[:-1])
        full_path.extend(nx.shortest_path(G, source=waypoints[-1], target=end, method="dijkstra"))
        calc_turns(full_path)
        print(f"Path with coordinates: {full_path}")

        segments = list(zip(full_path, full_path[1:]))

        # Use cross product to determine if the path is straight or not, positive indicates to the left, negative indicates to the right, 0 indicates straight (remember coords swapped)
        i = 1
        while i < len(segments):
            x1, y1 = segments[i-1][1][0] - segments[i-1][0][0], segments[i-1][1][1] - segments[i-1][0][1]
            x2, y2 = segments[i][1][0] - segments[i][0][0], segments[i][1][1] - segments[i][0][1]
            cross_product = (x1 * y2) - (y1 * x2)

            # Block detects whether the robot will go backwards by looking to see if the tuples in the pair are the same, it moves back one space and adds 2 to index var
            if segments[i][0] == segments[i][1]:
                path_directions.append("backwards")
                i += 2

                x1, y1 = segments[i-1][1][0] - segments[i-1][0][0], segments[i-1][1][1] - segments[i-1][0][1]
                x2, y2 = segments[i][1][0] - segments[i][0][0], segments[i][1][1] - segments[i][0][1]
                cross_product = (x1 * y2) - (y1 * x2)

                if cross_product > 0:
                    path_directions.append("right")
                    path_directions.append("forward")
                elif cross_product < 0:
                    path_directions.append("left")
                    path_directions.append("forward")
            elif cross_product > 0:
                path_directions.append("left")
                path_directions.append("forward")
            elif cross_product < 0:
                path_directions.append("right")
                path_directions.append("forward")
            else:
                path_directions.append("forward")
            i += 1

        # Print out directions list
        print(f"Directions to take: {path_directions}")
        # Draw it using the below
        draw_grid(G, full_path)

    else:
        # Find the shortest path from the start point to the end node
        path = nx.shortest_path(G, source=start, target=end, method="dijkstra")

        calc_turns(path)

        # Draw it using the below
        draw_grid(G, path)

def main():
    # List of coordinates of all the edges of the grid
    edges_numbering = {
        "1": [((0,0), (0,1))],
        "2": [((0,1), (0,2))],
        "3": [((0,2), (0,3))],
        "4": [((1,0), (1,1))],
        "5": [((1,1), (1,2))],
        "6": [((1,2), (1,3))],
        "7": [((2,0), (2,1))],
        "8": [((2,1), (2,2))],
        "9": [((2,2), (2,3))],
        "10": [((3,0), (3,1))],
        "11": [((3,1), (3,2))],
        "12": [((3,2), (3,3))],
        "13": [((0,0), (1,0))],
        "14": [((0,1), (1,1))],
        "15": [((0,2), (1,2))],
        "16": [((0,3), (1,3))],
        "17": [((1,0), (2,0))],
        "18": [((1,1), (2,1))],
        "19": [((1,2), (2,2))],
        "20": [((1,3), (2,3))],
        "21": [((2,0), (3,0))],
        "22": [((2,1), (3,1))],
        "23": [((2,2), (3,2))],
        "24": [((2,3), (3,3))]
    }
    # List of coordinates for all the boxes in the track for a total of 16, each represented by a 3x3 node area
    boxes_numbering = {
        "1" : (0,0),
        "2" : (0,1),
        "3" : (0,2),
        "4" : (0,3),
        "5" : (1,0),
        "6" : (1,1),
        "7" : (1,2),
        "8" : (1,3),
        "9" : (2,0),
        "10" : (2,1),
        "11" : (2,2),
        "12" : (2,3),
        "13" : (3,0),
        "14" : (3,1),
        "15" : (3,2),
        "16" : (3,3)
    }

    if int(input("1 if default, 0 else: ")) == 1:
        createGrid()

    else:
        x,y = input("Enter the coordinates of the starting point: ").split(",")
        starting_coords = (int(y),int(x))
        a,b = input("Enter the coordinates of the ending point: ").split(",")
        ending_coords = (int(b),int(a))

        missing_edges = []
        for i in range(8):
            missing_edges.append(edges_numbering[input("Enter an edge that is missing: ")])

        checkpoints = []
        for i in range(int(input("How many checkpoints: "))):
            checkpoints.append(boxes_numbering[input("Enter the boxes that are checkpoints: ")])

        # Note to self when continuing: find a way to add all these edges to a list or smth and then create a for loop that graphs all the data from the dictionary COMPLETE
        # Use: edges_numbering[edge_missing] as a parameter COMPLETE
        # Next, find a way to add the checkpoints, the process will be similar to the edge process, but this will require adjusting the Dijkstra algorithm a little
        createGrid(starting_coords, ending_coords, missing_edges, checkpoints)

if __name__ == "__main__":
    main()

