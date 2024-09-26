import networkx as nx
import matplotlib.pyplot as plt

# Parameters
n = 50  # Total number of nodes
m = 10  # Number of edges from a new node to existing nodes

# Generate a Barabási-Albert graph
graph = nx.barabasi_albert_graph(n, m)

# Draw the graph
nx.draw(graph, node_size=10, with_labels=False)
plt.title("Barabási-Albert Graph")
plt.show()