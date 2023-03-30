import networkx as nx
import utilities as util

df_reply = util.create_df_from_edge_list('network-data/higgs-reply_network.edgelist')
G_reply = util.create_graph_from_df(df_reply, edge_attr='Day')