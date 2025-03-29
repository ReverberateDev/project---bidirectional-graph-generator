import json
import os

# File paths
graph_file_path = 'resources/graph_adjacency_list.json'
coordinates_file_path = 'resources/coordinates.json'
output_file_path = 'resources/generated_map.cpp'

# Load the JSON files
with open(graph_file_path, 'r') as f:
    adjacency_list = json.load(f)

with open(coordinates_file_path, 'r') as f:
    coordinates = json.load(f)

# Helper function to determine the waypoint type and ID
def get_waypoint_info(node_name):
    if node_name.startswith('S'):
        return 'delivery_point', int(node_name[1:])
    elif node_name.startswith('P'):
        return 'pathfinding_point', int(node_name[1:])
    elif node_name.startswith('C'):
        return 'collection_point', int(node_name[1:])
    else:
        raise ValueError(f"Unknown waypoint type in node name: {node_name}")

# Start creating the C++ header file content
header_content = """
#include <vector>
#include <string>
#include <map>
#include "data_structure.hpp"
"""

# Creating adjacency list variable declaration
adj_list_code = "std::map<data_structure::waypoint, std::vector<data_structure::waypoint>> adjacency_list = {\n"

# Process each node in the graph
for node_name, neighbors in adjacency_list.items():
    node_type, node_id = get_waypoint_info(node_name)
    coordinates_of_node = coordinates.get(node_name, {"x": 0, "y": 0})
    x = coordinates_of_node["x"]
    y = coordinates_of_node["y"]

    # Create the waypoint for the current node
    waypoint_obj = f"data_structure::waypoint({x}, {y}, {node_id}, "
    if node_type == 'collection_point':
        waypoint_obj += "true, false, false"
    elif node_type == 'delivery_point':
        waypoint_obj += "false, true, false"
    elif node_type == 'pathfinding_point':
        waypoint_obj += "false, false, true"
    waypoint_obj += ")"

    # Add the waypoint to the adjacency list in C++ format
    adj_list_code += f"    {{ {waypoint_obj}, {{"

    # Add neighbors to the adjacency list
    for neighbor in neighbors:
        neighbor_type, neighbor_id = get_waypoint_info(neighbor)
        coordinates_of_neighbor = coordinates.get(neighbor, {"x": 0, "y": 0})
        nx = coordinates_of_neighbor["x"]
        ny = coordinates_of_neighbor["y"]

        neighbor_obj = f"data_structure::waypoint({nx}, {ny}, {neighbor_id}, "
        if neighbor_type == 'collection_point':
            neighbor_obj += "true, false, false"
        elif neighbor_type == 'delivery_point':
            neighbor_obj += "false, true, false"
        elif neighbor_type == 'pathfinding_point':
            neighbor_obj += "false, false, true"
        neighbor_obj += ")"

        adj_list_code += f"{neighbor_obj}, "

    # Remove last comma and add closing brackets
    adj_list_code = adj_list_code.rstrip(", ") + "}},\n"

# Close the adjacency list code
adj_list_code += "};\n"

# Combine header content and the adjacency list code
full_content = header_content + adj_list_code

# Write to the output C++ file
with open(output_file_path, 'w') as f:
    f.write(full_content)

print(f"C++ file generated successfully at {output_file_path}")
