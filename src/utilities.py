import networkx as nx
import pandas as pd
import numpy as np
import sys
import random
import csv
import os
import matplotlib.pyplot as plt

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
def get_subgraph(G, k=None, is_seed_node_most_connected=True):
    if k is None:
        k = G.number_of_nodes() // 5
    print('subgraph of: ' + str(k) + ' nodes')

    if is_seed_node_most_connected:
        seed_node = max(G.degree(), key=lambda x: x[1])[0]
    else:
        # Choosing a random node does not guarantee getting a subgraph of the desired size
        seed_node = random.choice(list(G.nodes()))
    # Initialize a queue for BFS and a set for visited nodes
    queue = [seed_node]
    visited = set([seed_node])
    # Initialize the subgraph with the starting node
    subgraph = nx.Graph()
    subgraph.add_node(seed_node)
    # While the subgraph has fewer than n nodes and the queue is not empty
    while len(subgraph) < k and queue:
        # Get the next node from the queue
        curr_node = queue.pop(0)
        # Add its neighbors that have not been visited to the queue and the subgraph
        for neighbor in G.neighbors(curr_node):
            if neighbor not in visited:
                if len(subgraph) >= k:
                    break
                visited.add(neighbor)
                subgraph.add_node(neighbor)
                subgraph.add_edge(curr_node, neighbor, day=G[curr_node][neighbor]["day"])
                queue.append(neighbor)
    return subgraph


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

# example of use: util.get_average_information_spreading_from_log("../log/mention.csv", "top3_out_degree_infected_nodes_time")
def get_average_information_spreading_from_log(log_file_path, metric):
    df = pd.read_csv(log_file_path, usecols=['metric', 'value'])
    # read desired value
    value = df[df["metric"] == metric].iloc[0]['value']
    # convert from string to numpy array
    value = np.array(eval(value))
    # Take the average of the n iterations passed as input
    return np.mean(value, axis=0), value

# example of use: util.plot_all_graph_metrics("../log/mention.csv", 0, 167, graph_name="Mention")
def plot_all_graph_metrics(log_file_path,  min_val, max_val, graph_name='No_name_given', color = {'baseline' : 'black', 'eigen' : 'g', 'out_degree' : 'r', 'followers' : 'orange'}):
    x_range = np.arange(min_val, max_val+2)
    out_degree_mean, out_degree  = get_average_information_spreading_from_log(log_file_path, "top3_out_degree_informed_nodes_time")
    eigen_mean, eigen = get_average_information_spreading_from_log(log_file_path, "top3_eigen_informed_nodes_time")
    baseline_mean, baseline = get_average_information_spreading_from_log(log_file_path, "baseline_informed_nodes_time")
    followers_mean, followers = get_average_information_spreading_from_log(log_file_path, "top3_followers_informed_nodes_time")
    plt.plot(x_range, out_degree_mean, label= "OutDegree" + ' informed nodes', alpha=0.8, c=color['out_degree'])
    plt.plot(x_range, eigen_mean, label="Eigen" + ' informed nodes', alpha=0.8, c=  color['eigen'])
    plt.plot(x_range, baseline_mean, label="Baseline" + ' informed nodes', alpha=0.8,c=  color['baseline'])
    plt.plot(x_range, followers_mean, label="Followers" + ' informed nodes', alpha=0.8,c=  color['followers'])


    for l in baseline:
        plt.plot(l, alpha =.1, color= color['baseline'])
    for l in eigen:
        plt.plot(l, alpha =.1, color= color['eigen'])
    for l in out_degree:
        plt.plot(l, alpha =.1, color= color['out_degree'])
    for l in followers:
        plt.plot(l, alpha =.1, color= color['followers'])
    

    plt.title("Starting Node comparison for " + graph_name + " network")
    plt.xlabel('Time (each time unit ≈ 60 minutes)')
    plt.ylabel('Ratio of nodes over all graph nodes')
    plt.legend(loc='upper left')