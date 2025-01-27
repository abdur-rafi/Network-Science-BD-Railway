from pyvis.network import Network
import networkx as nx

# Function to load and visualize a large network interactively
def visualize_gexf_network_interactive(file_path: str):
    print(f"Loading network from {file_path}...")
    G = nx.read_gexf(file_path)
    print(f"Network loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Create a Pyvis Network object
    net = Network(notebook=True, width="100%", height="800px")
    
    # Add all nodes and edges to the Pyvis Network
    net.from_nx(G)

    # Set physics for better interactive layout
    net.show_buttons(filter_=['physics'])
    net.set_options("""
    var options = {
      "physics": {
        "enabled": true,
        "solver": "barnesHut",
        "stabilization": {
          "iterations": 100
        }
      }
    }
    """)

    # Save and open in a browser
    output_file = "citation_network_interactive.html"
    net.show(output_file)
    print(f"Interactive network visualization saved as '{output_file}'.")

# File path to the .gexf file
file_path = "citation_network_20241105_233605.gexf"  # Replace with your actual file path

# Visualize the entire network interactively
visualize_gexf_network_interactive(file_path)
