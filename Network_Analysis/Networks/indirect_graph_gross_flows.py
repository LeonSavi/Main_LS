#%% NETWORK CHART 1: GROSS MONETARY AMOUNT

import networkx as nx
import matplotlib.pyplot as plt
#from pyvis.network import Network
import plotly.graph_objects as go
import plotly.express as px

network_data = (
        df
        )

G = nx.Graph()

for index, row in network_data.iterrows():
    
    rep_cp = row['counterparty1']
    oth_cp = row['counterparty2']
    mnt_am = row['moneteray_amount_exchanged']/(10**9)
    
    G.add_node(rep_cp)
    G.add_node(oth_cp)
    
    if G.has_edge(rep_cp, oth_cp):
        G.edges[rep_cp, oth_cp]['monetary_amount'] += mnt_am
    else:
        G.add_edge(rep_cp, oth_cp, monetary_amount=mnt_am)

dc = nx.degree_centrality(G)
bc = nx.betweenness_centrality(G,weight = 'monetary_amount')
ec = nx.eigenvector_centrality(G,weight = 'monetary_amount', max_iter = 1000, tol = 1e-06)

degree_centralities        = pd.DataFrame(dc.items(),columns=['counterparty', 'degree_centralities'])
w_betweenness_centralities = pd.DataFrame(bc.items(),columns=['counterparty', 'weighted_betweenness_centralities'])
eigenvector_centralities   = pd.DataFrame(ec.items(),columns=['counterparty', 'eigenvector_centralities'])

nodes_list =  list(G.nodes)
dict_nodes = {node:len(list(nx.neighbors(G, node))) for node in nodes_list}

df_links = (
    pd.DataFrame(dict_nodes.items(), columns=['counterparty', 'link_count'])
    .merge(degree_centralities, how = 'left', on = 'counterparty')
    #.merge(w_betweenness_centralities, how = 'left', on = 'counterparty')
    .merge(eigenvector_centralities, how = 'left', on = 'counterparty')
    )


#%% get attributes dictionaries

name_dict = {v['counterparty']:v['counterparty_LEGAL_NAME'] for _,v in df_links.iterrows()}
cntr_dict = {v['LEI']:v['COUNTRY'] for _,v in myRefEntities.iterrows() if v['LEI'] in nodes_list}
sect_dict = {v['LEI']:v['SECTOR'] for _,v in myRefEntities.iterrows() if v['LEI'] in nodes_list}

nsec_dict={}
for key,value in sect_dict.items():
    nsec_dict[key] = ?????.get(value)


nx.set_node_attributes(G, name_dict, 'LEI_name')
nx.set_node_attributes(G, sect_dict, 'SECTOR')
nx.set_node_attributes(G, cntr_dict, 'COUNTRY')
nx.set_node_attributes(G, nsec_dict, 'SECTOR_FIN')
nx.set_node_attributes(G, dist_dict, 'DIST_FIN')
nx.set_node_attributes(G, ec, 'Eigenvector_C')
#nx.set_node_attributes(G, bc, 'Betweenness_C')
nx.set_node_attributes(G, dc, 'Degree_C')

#%% SUBGRAPH

S = G.copy()

# removing non financial CPs and isolated edges (first time)
lst_none = [n for n,d in S.nodes(data= True) if d['SECTOR_FIN'] is None]
S.remove_nodes_from(lst_none)
S.remove_nodes_from(list(nx.isolates(S)))

# set arbitrary threshold 0.9., remove edges below that monetary amount
# LS: possible improvements: if a node has at least one edge with that monetary amount keep all the edges of that node. 
monetary_amounts = sorted([float(e['monetary_amount']) for n,v,e in S.edges(data=True)], reverse = True)
#quantile_threshold = np.quantile(monetary_amounts, q = 0.975)
quantile_threshold = 4
edges_to_rem =  [(n,v) for n,v,e in S.edges(data=True) if e['monetary_amount'] < quantile_threshold]

# Keep edges above the threshold, and remove isolated nodes
S.remove_edges_from(edges_to_rem) # remove edges below 99 percentile
S.remove_nodes_from(list(nx.isolates(S))) # remove nodes without edges

pos = {key: list(value) for key, value in nx.kamada_kawai_layout(S,scale = 4).items()}

nx.set_node_attributes(S, pos, 'pos')

#%% Set nodes conditions

sector_symbols = {
    'CCP': 'circle',
    'Bank': 'square',
    'Inv. Firm': 'triangle-up',
    'Foreign Funds': 'diamond',
    'Central Bank': 'cross',
    'Insurance': 'star',
    'AIF': 'x',
    'Pension Fund': 'triangle-down',
    'CSD': 'hexagon',
    'UCIT': 'pentagon',
    'Non Financial': 'star-square'
}

reverse_symbols = {v:x for x,v in sector_symbols.items()}

#%%
# colorscale options
#'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
#'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
#'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |

##################
###### EDGES #####
##################

# edges position

mnt_mnt = [float(e['monetary_amount']) for _,_,e in S.edges(data=True)]
norm_mnt = [(x -  min(mnt_mnt)) / (max(mnt_mnt) -  min(mnt_mnt)) for x in mnt_mnt]

# Convert normalized monetary values to colors based on the colorscale
edge_color_scale = [[0, 'blue'], [1, 'red']]  # Customize the colors as desired
edge_colors = [edge_color_scale[int(val * (len(edge_color_scale) - 1))][1] for val in norm_mnt]

edge_x = []
edge_y = []
edge_colors = []

for edge in S.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_colors.append(norm_mnt.pop(0))  # Pop the first value from the normalized_mnt list

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='rgba(0,0,0,0.2)'),
    marker=dict(color=edge_colors, colorscale=edge_color_scale, colorbar=dict(title='Monetary Amount Volume')),
    hoverinfo='none',
    mode='lines',
    showlegend = False
)

##################
###### NODES #####
##################

# nodes position
node_x = []
node_y = []
for node in S.nodes():
    x, y = S.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_eigen     = [d['Eigenvector_C'] for _,d in S.nodes(data=True)]
node_eigen_txt = ['the Eigenvector_centrality is '+str(d['Eigenvector_C']) for _,d in S.nodes(data=True)]

    
node_adjacencies = [len(adjacencies[1]) for _, adjacencies in enumerate(S.adjacency())]
node_text        = ['# of connections: '+str(len(adjacencies[1])) for _, adjacencies in enumerate(S.adjacency())]
node_adj_sizes   = [10 + (40 - 10) * (adjacency - min(node_adjacencies)) / (max(node_adjacencies) - min(node_adjacencies)) for adjacency in node_adjacencies]


node_symbols = [sector_symbols.get(S.nodes[node]['SECTOR_FIN']) for node in S.nodes()]

#setting nodes

node_traces = []

for sector in set(nx.get_node_attributes(S, 'SECTOR_FIN').values()):
    # Filter nodes for the current sector
    sector_nodes = [node for node in S.nodes() if S.nodes[node]['SECTOR_FIN'] == sector]
    sector_indices = [node_x.index(S.nodes[node]['pos'][0]) for node in sector_nodes]

    sz = [node_adj_sizes[i] for i in sector_indices]
    cl = [round(node_eigen[i], 3) for i in sector_indices]
    sm = [node_symbols[i] for i in sector_indices]
    txt = [node_eigen_txt[i] for i in sector_indices]

    xpos = [node_x[i] for i in sector_indices]
    ypos = [node_y[i] for i in sector_indices]

    # Create a new trace for the current sector
    trace = go.Scattergl(
        x=xpos,
        y=ypos,
        mode='markers',
        name=sector,
        marker=dict(
            size=sz,
            color=cl,
            colorscale='RdBu',
            reversescale=False,
            showscale = True,
            cmin = min(node_eigen),
            cmax = max(node_eigen),
            colorbar=dict(
                thickness=15,
                title='Eigenvector centrality',
                xanchor='left',
                titleside='right',
                xpad=5                
            ),
            line_width=2,
            symbol=sm,
        ),
        hoverinfo='text',
        showlegend=True,
        text=txt,
    )

    # Append the trace to the list
    node_traces.append(trace)


# Create the figure
fig = go.Figure(data=[edge_trace, *node_traces],  # Use *node_traces to unpack the list of traces
                layout=go.Layout(
                    title='NETWORK CHART: GROSS FLOWS',
                    titlefont_size=16,
                    showlegend=True,  # Show the legend
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    #coloraxis=dict(colorbar=clr_bar),
                    legend=dict(  # Custom legend configuration for the symbols
                        x=0.1,
                        y=0.9,
                        bgcolor='rgba(255, 255, 255, 0.7)',
                        bordercolor='black',
                        borderwidth=1,
                        traceorder='normal',
                        font=dict(
                            family='Arial',
                            size=10,
                            color='black'
                        )
                    )

                )
            )

fig.write_html('graph.html')
