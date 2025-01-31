import os
import json
import networkx as nx

# Directory containing the JSON files
input_dir = "output/"
output_network_file = "train_network_jp.gexf"

# Initialize a graph
G = nx.Graph()  # Use DiGraph if you want directed edges; otherwise, use Graph()

# Function to process a JSON file and add nodes and edges to the graph
def process_json(file_path, graph):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        stations = data.get("data", [])
        
        # Add nodes and edges for consecutive stations
        for i in range(len(stations) - 1):
            current_station = stations[i]["STATION_NAME_EN_M"]
            next_station = stations[i + 1]["STATION_NAME_EN_M"]
            
            # Add nodes
            graph.add_node(current_station)
            graph.add_node(next_station)
            
            # Add edge between consecutive stations
            graph.add_edge(current_station, next_station)

# Process all JSON files in the directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(input_dir, file_name)
        process_json(file_path, G)

# Save the resulting graph to a GEXF file
nx.write_gexf(G, output_network_file)

print(f"Network successfully built and saved to {output_network_file}")
