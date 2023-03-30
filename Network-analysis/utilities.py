import networkx as nx
import pandas as pd

def create_graph_from_df(df, edge_attr=None, source='SourceID', target='TargetID'):
    return nx.from_pandas_edgelist(df, source=source, target=target, edge_attr=edge_attr)

def create_df_from_edge_list(edgeListPath, names=['SourceID','TargetID','Day']):
    return pd.read_csv(edgeListPath, sep='\s+', header=None, names=names)