import tkinter as tk
from tkinter import simpledialog
import math
import json

rad = 20  # radius of the node
inf = float(1e18)

class node:
    def __init__(self, x, y, name = None, tag = None):
        self.x = x
        self.y = y
        self.name = name
        self.tag = f"node_{self.name}"
    
    def displayNode(self, canvas):
        x1 = self.x - rad
        y1 = self.y - rad
        x2 = self.x + rad
        y2 = self.y + rad
        canvas.create_oval(x1, y1, x2, y2, fill = "skyblue", tags = self.tag)
        canvas.create_text(self.x, self.y, text=self.name, font=("Arial", 12), tags = self.tag)
        return


class edge:
    def __init__(self, start_node = None, end_node = None, tag = None):
        self.start_node = start_node
        self.end_node = end_node
    def setTag(self):
        self.tag = f"edge_{self.start_node.name}_{self.end_node.name}"
    
    def displayEdge(self, canvas):
        x1 = self.start_node.x
        y1 = self.start_node.y
        x2 = self.end_node.x
        y2 = self.end_node.y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        unit_dx = (x2 - x1) / distance
        unit_dy = (y2 - y1) / distance

        x1 += unit_dx * rad
        y1 += unit_dy * rad
        x2 -= unit_dx * rad
        y2 -= unit_dy * rad

        canvas.create_line(x1, y1, x2, y2, width = 2, tags = self.tag)
        return

class GraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Builder")

        # Make the window full screen
        self.root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Make canvas expand with window resizing

        self.nodes = list()
        self.edges = list()

        self.canvas.bind("<Button-1>", self.createNode)
        self.canvas.bind("<ButtonPress-3>", self.startEdge)
        self.canvas.bind("<ButtonRelease-3>", self.endEdge)
        self.canvas.bind("<Button-2>", self.deleteItem)
        
        # Fix for focusing on the canvas and key press events
        self.canvas.focus_set()  # Make sure the canvas can receive key press events
        self.canvas.bind("<a>", self.outputData)  # Ensure 'a' key triggers outputData

    def getNodeName(self):
        name = simpledialog.askstring("Node Name", "Enter node name:")
        return name

    def getClosestNode(self, x, y):
        closest_node =(inf, None)
        for node in self.nodes:
            dx = abs(x - node.x)
            dy = abs(y - node.y)
            dd = math.sqrt(dx * dx + dy * dy)
            closest_node = min(closest_node, (dd, node))
        return closest_node[1]

    def getDistanceBetweenItem(self, x, y, item):
        """Calculate distance from (x, y) to the given item (either node or edge)."""
        if isinstance(item, node):
            # For nodes, calculate Euclidean distance to the center of the node
            dx = x - item.x
            dy = y - item.y
            return math.sqrt(dx * dx + dy * dy)
        
        elif isinstance(item, edge):
            # For edges, calculate the distance from the point (x, y) to the line segment
            x1 = item.start_node.x
            y1 = item.start_node.y
            x2 = item.end_node.x
            y2 = item.end_node.y
            
            # If the edge is a point (same start and end node), calculate distance to the point
            if (x1 == x2 and y1 == y2):
                return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

            # Calculate the line segment length
            line_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            
            # Project point (x, y) onto the line and calculate the perpendicular distance
            t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / line_len ** 2))
            closest_x = x1 + t * (x2 - x1)
            closest_y = y1 + t * (y2 - y1)
            
            # Return the Euclidean distance from the point to the closest point on the line
            return math.sqrt((x - closest_x) ** 2 + (y - closest_y) ** 2)

        return inf  # Return infinity if the item is neither a node nor an edge

    def createNode(self, event):
        #create node
        self.current_node = node(event.x, event.y, self.getNodeName())

        self.nodes.append(self.current_node)
        self.current_node.displayNode(self.canvas)

    def startEdge(self, event):
        #create start of edge
        self.current_edge = edge(self.getClosestNode(event.x, event.y), None)
    def endEdge(self, event):
        #create end of edge
        self.current_edge.end_node = self.getClosestNode(event.x, event.y)
        self.current_edge.setTag()
        self.edges.append(self.current_edge)
        self.current_edge.displayEdge(self.canvas)
    def deleteItem(self, event):
        print("Deleting item")
        best = (inf, None)

        # Find the closest node
        for node in self.nodes:
            best = min(best, (self.getDistanceBetweenItem(event.x, event.y, node), node))

        # Find the closest edge
        for edge in self.edges:
            best = min(best, (self.getDistanceBetweenItem(event.x, event.y, edge), edge))

        # If an item is found (best[1] is not None), delete it from canvas and the list
        if best[1]:
            self.canvas.delete(best[1].tag)  # Delete from the canvas

            # If it's a node, remove it from the nodes list
            if isinstance(best[1], node):
                self.nodes.remove(best[1])
            # If it's an edge, remove it from the edges list
            elif isinstance(best[1], edge):
                self.edges.remove(best[1])

            print(f"Deleted: {best[1]}")
    def outputData(self, event):
        print("Outputting data")
        # Create a dictionary to store the adjacency list
        adj_list = {}

        # Traverse the edges list to build the adjacency list
        for edge in self.edges:
            # Ensure both nodes in the edge are in the dictionary
            if edge.start_node.name not in adj_list:
                adj_list[edge.start_node.name] = []
            if edge.end_node.name not in adj_list:
                adj_list[edge.end_node.name] = []
            
            # Add the neighbor relations (since this is an undirected graph)
            adj_list[edge.start_node.name].append(edge.end_node.name)
            adj_list[edge.end_node.name].append(edge.start_node.name)

        # Save the adjacency list as a JSON file
        with open("resources/graph_adjacency_list.json", "w") as json_file:
            json.dump(adj_list, json_file, indent=4)
        self.root.quit()

root = tk.Tk()
app = GraphGUI(root)
root.mainloop()
