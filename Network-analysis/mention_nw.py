import networkx as nx
import utilities as util

df_mention = util.create_df_from_edge_list('network-data/higgs-mention_network.edgelist')
G_mention = util.create_graph_from_df(df_mention)