import networkx as nx
import pandas as pd

def create_graph_from_df(df):
    return nx.from_pandas_edgelist(df,source='SourceID',target='TargetID',edge_attr='Day')

def create_df_from_edge_list(edgeListPath):
    return pd.read_csv(edgeListPath, sep='\s+', header=None, names=['SourceID','TargetID','Day'])