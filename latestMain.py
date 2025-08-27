import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
import math
#globals
stage = 0
box_width = 72
global starting_coords,ending_coords
starting_coords=(-1,-1)
ending_coords=(-1,-1)
global labels
global missing_edges
global root
missing_edges = []
global checkpoints
checkpoints = []
labels = ["Select starting point","Select ending point","select edges","select boxes"]
def grid():
     for i in range(4):
            for j in range(4):
                canvas.create_rectangle(box_width*(i),box_width*(j),box_width*(i+1),box_width*(j+1),outline = "black",width=box_width/36)

def nextCallback():
    global stage
    stage+=1
    

    if(stage < len(labels)):
        label.config(text=labels[stage])
    else:
        root.destroy()
    pass
def reset():
    if(stage >= 0):
        canvas.delete("all")
        grid()
        canvas.create_oval((starting_coords[1]+0.4)*box_width,(starting_coords[0]+0.4)*box_width,(starting_coords[1]+0.6)*box_width,(starting_coords[0]+0.6)*box_width,fill="green")
        print(starting_coords)
    if(stage >= 1):
        canvas.create_oval((ending_coords[1]+0.4)*box_width,(ending_coords[0]+0.4)*box_width,(ending_coords[1]+0.6)*box_width,(ending_coords[0]+0.6)*box_width,fill="red")
    if(stage >= 3):
        for checkpoint in checkpoints:
            canvas.create_rectangle(box_width*(checkpoint[1]),box_width*(checkpoint[0]),box_width*(checkpoint[1]+1),box_width*(checkpoint[0]+1),outline = "BLUE",width=box_width/12)
    if(stage >= 2):
        for edge in missing_edges:
            change = ((edge[0][1][0]-edge[0][0][0])*2/3+1/6,(edge[0][1][1]-edge[0][0][1])*2/3+1/6)
            location=(((edge[0][1][1]+edge[0][0][1])/2+0.5),((edge[0][1][0]+edge[0][0][0])/2+0.5))
            canvas.create_rectangle((location[0]-change[0]/2)*box_width,(location[1]-change[1]/2)*box_width,(location[0]+change[0]/2)*box_width,(location[1]+change[1]/2)*box_width,fill="brown")
            print(location)
            print(change)

            
def gridClick(event):
    global starting_coords
    global ending_coords
    if(stage == 0):
        starting_coords = (math.floor(event.y/box_width),math.floor(event.x/box_width))
    elif(stage == 1):
        ending_coords = (math.floor(event.y/box_width),math.floor(event.x/box_width))
    elif(stage == 2):
        global missing_edges
        coords_help=[[-1,0],
                    [1,0],
                    [0,-1],
                    [0,1]]
        min_finder = [event.x%box_width,box_width-event.x%box_width,event.y%box_width,box_width-event.y%box_width]
        coords_add = coords_help[min_finder.index(min(min_finder))]
        coords_near = ((math.floor(event.y/box_width),math.floor(event.x/box_width)),(math.floor(event.y/box_width)+coords_add[1],math.floor(event.x/box_width+coords_add[0])))
        coords_fin = [tuple(sorted(coords_near))]

        if(coords_fin in missing_edges):
            missing_edges.remove(coords_fin)
        else:
            missing_edges.append(coords_fin)
        pass
    elif(stage == 3):
        coord_set = (math.floor(event.y/box_width),math.floor(event.x/box_width))
        if(coord_set in checkpoints):
            checkpoints.remove(coord_set)
        else:
            checkpoints.append(coord_set)
    reset()

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
                path_directions.append("moveBackward(forward_distance+backwards_offset); ")
                i += 2

                x1, y1 = segments[i-1][1][0] - segments[i-1][0][0], segments[i-1][1][1] - segments[i-1][0][1]
                x2, y2 = segments[i][1][0] - segments[i][0][0], segments[i][1][1] - segments[i][0][1]
                cross_product = (x1 * y2) - (y1 * x2)

                if cross_product > 0:
                    path_directions.append("turnRight(right_angle);")
                    path_directions.append("moveForward(forward_distance);")
                elif cross_product < 0:
                    path_directions.append("turnLeft(left_angle);")
                    path_directions.append("moveForward(forward_distance);")
            elif cross_product > 0:
                path_directions.append("turnLeft(left_angle);")
                path_directions.append("moveForward(forward_distance);")
            elif cross_product < 0:
                path_directions.append("turnRight(right_angle);")
                path_directions.append("moveForward(forward_distance);")
            else:
                path_directions.append("moveForward(forward_distance);")
            i += 1

        # Print out directions list
        print(f"Directions to take:")
        for direction in path_directions:
            print(direction)
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
   
    
    # Start the GUI event loop
    if int(input("1 if default, 0 else: ")) == 1:
        createGrid()

    else:
        global root
        root = tk.Tk()
        global box_width
        
        # Create a label widget
        global label
        label = tk.Label(root, text='Select start point')
        label.place(x=0,y=0)
        global canvas
        canvas = tk.Canvas(root,bg="white",height=4*box_width,width=4*box_width)

        root.geometry('576x576')
        grid()
        canvas.bind("<Button-1>", gridClick)
        canvas.place(x=box_width*2,y= box_width)
        
        next = tk.Button(root,text="Next", command=nextCallback)
        next.place(relx=1.0, rely=1.0, anchor="se")
        root.mainloop()



        '''x,y = input("Enter the coordinates of the starting point: ").split(",")
        
        starting_coords = (int(y),int(x))
        a,b = input("Enter the coordinates of the ending point: ").split(",")
        ending_coords = (int(b),int(a))
        global missing_edges
        missing_edges = []
        for i in range(8):
            missing_edges.append(edges_numbering[input("Enter an edge that is missing: ")])

        checkpoints = []
        for i in range(int(input("How many checkpoints: "))):
            checkpoints.append(boxes_numbering[input("Enter the boxes that are checkpoints: ")])
        '''
        # Note to self when continuing: find a way to add all these edges to a list or smth and then create a for loop that graphs all the data from the dictionary COMPLETE
        # Use: edges_numbering[edge_missing] as a parameter COMPLETE
        # Next, find a way to add the checkpoints, the process will be similar to the edge process, but this will require adjusting the Dijkstra algorithm a little
        createGrid(starting_coords, ending_coords, missing_edges, checkpoints)

if __name__ == "__main__":
    main()

