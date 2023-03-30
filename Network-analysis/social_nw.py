import networkx as nx
import utilities as util

df_social_network = util.create_df_from_edge_list('network-data/higgs-social_network.edgelist')
G_social_network = util.create_graph_from_df(df_social_network)
