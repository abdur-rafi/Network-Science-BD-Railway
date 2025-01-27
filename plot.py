import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Function to load the network, compute degree distribution, and plot it
def plot_degree_distribution(file_path: str):
    # Load the .gexf file as a NetworkX graph
    print(f"Loading network from {file_path}...")
    G = nx.read_gexf(file_path)
    print(f"Network loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Compute the degree of each node
    degrees = [deg for node, deg in G.degree()]
    
    # Calculate degree distribution (frequency of each degree)
    degree_count = {}
    for degree in degrees:
        if degree in degree_count:
            degree_count[degree] += 1
        else:
            degree_count[degree] = 1
    
    # Extract degree values and their frequencies
    degree_values = list(degree_count.keys())
    frequency_values = list(degree_count.values())
    
    # Plotting the degree distribution
    plt.figure(figsize=(8, 6))
    plt.bar(degree_values, frequency_values, color="skyblue")
    plt.title("Degree Distribution")
    plt.xlabel("Degree (Number of connections)")
    plt.ylabel("Frequency (Number of nodes)")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

    # Print related statistics
    print("\nDegree Distribution Statistics:")
    print(f"Average degree: {np.mean(degrees)}")
    print(f"Maximum degree: {max(degrees)}")
    print(f"Minimum degree: {min(degrees)}")
    print(f"Degree variance: {np.var(degrees)}")

# File path to the .gexf file
file_path = "citation_network_20241105_233605.gexf"  # Replace with your actual file path

# Call the function to plot degree distribution and print stats
plot_degree_distribution(file_path)
