import networkx as nx
import matplotlib.pyplot as plt

def create_grid_graph(size, edge, checkpoints):
    G = nx.grid_2d_graph(size, size)

    #Can remove edges here to represent walls, but I forgot how to do that lol
    #Add the part about checkpoints to this and make the conditional a compound conditional
    if edge is not None:
        for coordinate in edge:
            G.remove_edge(coordinate[0][0], coordinate[0][1])
            G.remove_edge(coordinate[1][0], coordinate[1][1])
            G.remove_edge(coordinate[2][0], coordinate[2][1])


    return G

def draw_grid(G, path=None):
    pos = {(x, y): (y, -x) for x, y in G.nodes()}

    color_map = []
    for node in G.nodes():
        x, y = node
        if ((x // 3) + (y // 3)) % 2 == 0:
            color_map.append('orange')  # Replace 'color1' with your ORANGE
        else:
            color_map.append("lightblue")  # Replace 'color2' with another LIGHT BLUE

    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=600)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green")
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="green", width=2)

    plt.show()

#The point is that path contains a list of tuples that represent the coordinates of the path it takes
#False will represent the y-axis, True will represent the x-axis
def calc_turns(path, num_turn=0, temp=False):
    axis = path[0][1] == path[1][1]

    for i in range(1,len(path)-1):
        temp = path[i][1] == path[i+1][1]
        if temp is not  axis:
            num_turn+=1
            axis=temp
        print(f"Coordinates of node {i}: {path[i]}")
    print(f"Turned: {num_turn}")

def calc_weight(path, turns=None, turn_time=4, travel_time=1):
    ...

def createGrid(start_x=1, start_y=0, end_x=10, end_y=10, edge=None, checkpoints=None):
    #Initialize the graph
    G = create_grid_graph(12, edge, checkpoints)

    #Find the shortest path from the start point to the end node
    path = nx.shortest_path(G, source=(int(start_y), int(start_x)), target=(int(end_y), int(end_x)), method='dijkstra')

    calc_turns(path)

    #Draw it
    draw_grid(G, path)

def main():
    #List of coordinates of all the edges of the grid
    edges_numbering = {
        "1" : [((0,2),(0,3)), ((1,2),(1,3)), ((2,2),(2,3))],
        "2" : [((0,5),(0,6)), ((1,5),(1,6)), ((2,5),(2,6))],
        "3" : [((0,8),(0,9)), ((1,8),(1,9)), ((2,8),(2,9))],
        "4" : [((3,2),(3,3)), ((4,2),(4,3)), ((5,2),(5,3))],
        "5" : [((3,5),(3,6)), ((4,5),(4,6)), ((5,5),(5,6))],
        "6" : [((3,8),(3,9)), ((4,8),(4,9)), ((5,8),(5,9))],
        "7" : [((6,2),(6,3)), ((7,2),(7,3)), ((8,2),(8,3))],
        "8" : [((6,5),(6,6)), ((7,5),(7,6)), ((8,5),(8,6))],
        "9" : [((6,8),(6,9)), ((7,8),(7,9)), ((8,8),(8,9))],
        "10" : [((9,2),(9,3)), ((10,2),(10,3)), ((11,2),(11,3))],
        "11" : [((9,5),(9,6)), ((10,5),(10,6)), ((11,5),(11,6))],
        "12" : [((9,8),(9,9)), ((10,8),(10,9)), ((11,8),(11,9))],

        "13" : [((2,0),(3,0)), ((2,1),(3,1)), ((2,2),(3,2))],
        "14" : [((2,3),(3,3)), ((2,4),(3,4)), ((2,5),(3,5))],
        "15" : [((2,6),(3,6)), ((2,7),(3,7)), ((2,8),(3,8))],
        "16" : [((2,9),(3,9)), ((2,10),(3,10)), ((2,11),(3,11))],
        "17" : [((5,0),(6,0)), ((5,1),(6,1)), ((5,2),(6,2))],
        "18" : [((5,3),(6,3)), ((5,4),(6,4)), ((5,5),(6,5))],
        "19" : [((5,6),(6,6)), ((5,7),(6,7)), ((5,8),(6,8))],
        "20" : [((5,9),(6,9)), ((5,10),(6,10)), ((5,11),(6,11))],
        "21" : [((8,0),(9,0)), ((8,1),(9,1)), ((8,2),(9,2))],
        "22" : [((8,3),(9,3)), ((8,4),(9,4)), ((8,5),(9,5))],
        "23" : [((8,6),(9,6)), ((8,7),(9,7)), ((8,8),(9,8))],
        "24" : [((8,9),(9,9)), ((8,10),(9,10)), ((8,11),(9,11))]
    }
    #List of coordinates for all of the boxes in the track for a total of 16, each represented by a 3x3 node area
    boxes_numbering = {
        "1" : {(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)},
        "2" : {(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)},
        "3" : {(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)},
        "4" : {(0,9), (0,10), (0,11), (1,9), (1,10), (1,11), (2,9), (2,10), (2,11)},
        "5" : {(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)},
        "6" : {(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)},
        "7" : {(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)},
        "8" : {(3,9), (3,10), (3,11), (4,9), (4,10), (4,11), (5,9), (5,10), (5,11)},
        "9" : {(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)},
        "10" : {(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)},
        "11" : {(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)},
        "12" : {(6,9), (6,10), (6,11), (7,9), (7,10), (7,11), (6,9), (6,10), (6,11)},
        "13" : {(9,0), (9,1), (9,2), (10,0), (10,1), (10,2), (11,0), (11,1), (11,2)},
        "14" : {(9,3), (9,4), (9,5), (10,3), (10,4), (10,5), (11,3), (11,4), (11,5)},
        "15" : {(9,6), (9,7), (9,8), (10,6), (10,7), (10,8), (11,6), (11,7), (11,8)},
        "16" : {(9,9), (9,10), (9,11), (10,9), (10,10), (10,11), (11,9), (11,10), (11,11)}
    }

    if int(input("1 if default, 0 else: ")) == 1:
        createGrid()
    else:
        x,y = input("Enter the coordinates of the starting point: ").split(",")
        a,b = input("Enter the coordinates of the ending point: ").split(",")

        missing_edges = []
        for i in range(8):
            missing_edges.append(edges_numbering[input("Enter an edge that is missing: ")])

        checkpoints = []
        for i in range(4):
            checkpoints.append(boxes_numbering[input("Enter the boxes that are checkpoints: ")])

        # Note to self when continuing: find a way to add all these edges to a list or smth and then create a for loop that graphs all the data from the dictionary COMPLETE
        # use: edges_numbering[edge_missing] as a parameter COMPLETE
        #Next, find a way to add the checkpoints, the process will be similar to the edge process, but this will require adjusting the Dijkstra algorithm a little
        createGrid(x, y, a, b, missing_edges, checkpoints)

if __name__ == "__main__":
    main()

