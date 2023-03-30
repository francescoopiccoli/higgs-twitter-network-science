import networkx as nx
import utilities as util

df_retweet = util.create_df_from_edge_list('network-data/higgs-retweet_network.edgelist')
G_retweet = util.create_graph_from_df(df_retweet)