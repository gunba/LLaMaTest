import os
import csv
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from community import community_louvain

# Set the working directory to the location of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the CSV file
with open('reviews_tags.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = list(csv_reader)

# Create a Counter to count the occurrences of each tag
tag_counter = Counter()

# Iterate over the data and count the occurrences of each tag
for item in data:
    tag = item['tags']
    tag_counter[tag] += 1

# Set the minimum occurrence count threshold
min_occurrence = 100

# Set the minimum degree threshold
min_degree = 100

# Create an empty graph
G = nx.Graph()

# Create a dictionary to store tags for each recommendationid
recommendation_tags = {}

# Iterate over the data and store tags for each recommendationid
for item in data:
    recommendationid = item['recommendationid']
    tag = item['tags']
    
    # Only consider tags that meet the minimum occurrence count threshold
    if tag_counter[tag] >= min_occurrence:
        if recommendationid not in recommendation_tags:
            recommendation_tags[recommendationid] = []
        recommendation_tags[recommendationid].append(tag)

# Iterate over the recommendation_tags dictionary and add edges to the graph
for recommendationid, tags in recommendation_tags.items():
    # Add edges between tags with the same recommendationid
    for i in range(len(tags)):
        for j in range(i+1, len(tags)):
            if G.has_edge(tags[i], tags[j]):
                G[tags[i]][tags[j]]['weight'] += 1
            else:
                G.add_edge(tags[i], tags[j], weight=1)

# Remove nodes with a degree below the minimum threshold
low_degree_nodes = [node for node, degree in dict(G.degree()).items() if degree < min_degree]
G.remove_nodes_from(low_degree_nodes)

# Check if the graph has any nodes
if not G.nodes():
    print("The graph is empty. No nodes found.")
else:
    # Apply community detection using the Louvain algorithm
    partition = community_louvain.best_partition(G)

    # Create a dictionary to store the community for each node
    node_community = {}
    for node, comm in partition.items():
        node_community[node] = comm

    # Visualize the graph using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 12))

    # Draw the graph using the Fruchterman-Reingold layout
    pos = nx.spring_layout(G, k=0.5, iterations=100)

    # Calculate the size of each node based on its degree with increased variance
    max_degree = max(dict(G.degree()).values())
    node_sizes = [3000 * (G.degree(node) / max_degree) ** 7 for node in G.nodes()]

    # Draw nodes with colors based on their community
    for comm in set(node_community.values()):
        comm_nodes = [node for node in G.nodes() if node_community[node] == comm]
        nx.draw_networkx_nodes(G, pos, nodelist=comm_nodes, node_size=[node_sizes[list(G.nodes()).index(node)] for node in comm_nodes],
                               node_color=plt.cm.Set1(comm), alpha=0.8, ax=ax)

    # Draw edges with reduced transparency
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.1, ax=ax)

    # Draw node labels with Segoe UI or DIN font
    nx.draw_networkx_labels(G, pos, font_size=16, font_family='Segoe UI', ax=ax)

    # Customize the plot
    ax.axis('off')
    plt.title('Tag Co-occurrence Network', fontsize=48, fontweight='bold', fontname='Segoe UI')

    # Display the plot
    plt.tight_layout()
    plt.show()