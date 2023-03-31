import networkx as nx
import pandas as pd
import numpy as np
import sys
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