import networkx as nx
import pandas as pd
import numpy as np
import sys
import random
import csv
import os

sys.path.append('../')
print(sys.path)

def create_graph_from_df(df, edge_attr=None, source='SourceID', target='TargetID', isDirected=False):
    create_using = None
    if isDirected: 
        create_using = nx.DiGraph() 
    return nx.from_pandas_edgelist(df, source=source, target=target, edge_attr=edge_attr, create_using=create_using)

def create_df_from_edge_list(edgeListPath, names=['SourceID','TargetID','Day']):
    return pd.read_csv(edgeListPath, sep='\s+', header=None, names=names)

def get_avg_degree(G):
    return np.mean(list(dict(G.degree()).values()))

def get_var_degree_distribution(G):
    return np.var(list(dict(G.degree()).values()))

def get_degree_distribution(G):
    degree_sequence = sorted([d for _, d in G.degree()], reverse=True)
    degree_count = {}
    for degree in degree_sequence:
        degree_count[degree] = degree_count.get(degree, 0) + 1
    return degree_count


def load_activity_time(path, names=['SourceID', 'TargetID', 'Timestamp', 'Type']):
    return pd.read_csv(path, sep='\s+', header=None, names=names)


# Get a subgraph of n nodes, where each node is connected to at least one node in the subgraph
def get_subgraph(G, k, is_seed_node_most_connected=False):
    if is_seed_node_most_connected:
        seed_node = max(G.degree, key=lambda x: x[1])[0]
    else:
        seed_node = random.choice(list(G.nodes()))

    subgraph = nx.ego_graph(G, seed_node)
    # Keep adding nodes until the subgraph has n nodes
    while len(subgraph) < k:
        # Select a random node from the subgraph
        node = random.choice(list(subgraph.nodes()))
        # Add its neighbors that are not already in the subgraph
        neighbors = [n for n in G.neighbors(node) if n not in subgraph]
        subgraph.add_nodes_from(neighbors)

    return G.subgraph(subgraph.nodes())


def print_and_log(network_name, metric_name, metric_value):
    current_dir = os.getcwd()
    os.chdir('../') # Assuming that the file from which this function is called is in a subfolder of the root folder
    print('(' + network_name + ') ' + metric_name + ': ' + str(metric_value))
    sys.stdout.flush()
    with open('log/' + network_name + '.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if csvfile.tell() == 0:
            writer.writerow(['metric', 'value'])

        writer.writerow([metric_name, metric_value])
    os.chdir(current_dir)