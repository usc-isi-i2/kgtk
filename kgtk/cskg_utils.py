import pandas as pd # type: ignore
from copy import copy
from collections import defaultdict
import csv
import sys
csv.field_size_limit(sys.maxsize)

def combine_dicts(dicts):
    new_dict=defaultdict(set)
    for d in dicts:
        for k in d.keys():
            new_dict[k] = new_dict[k] | set(d[k])
    for k, v in new_dict.items():
        v=list(v)
    return dict(new_dict)

def merge_and_deduplicate(x):
    return ','.join(list(set(x.split(','))))

def deduplicate_with_transformations(df, join_columns, transformations={'label': ','.join, 'aliases': ','.join, 'pos': ','.join, 'datasource': ','.join, 'other': ','.join}):
    grouped=df.groupby(join_columns, as_index=False).agg(transformations)
    for col in transformations.keys():
        if col not in ['other', 'weight']:
            grouped[col] = grouped[col].apply(merge_and_deduplicate)
#        elif col=='other':
#            grouped[col] = grouped[col].apply(combine_dicts)

    print(grouped)
    return grouped

def append_df_with_missing_nodes(base_df, missing_nodes, datasource, node_columns):
    """
    Complement a nodes dataframe with missing nodes, represented with minimal info.
    """
    print(missing_nodes)
    rows=[]
    for n in missing_nodes:
        a_row=[n, "", "", "", datasource, {}]
        rows.append(a_row)
    new_df=pd.DataFrame(rows, columns=node_columns)
    combined_nodes = pd.concat([base_df, new_df])
    print(len(combined_nodes), 'nodes')

    return combined_nodes

def flatten_multiple_values(tmp_edges_df, col):
    """
    Function that handles multiple, comma-separated values of a column by using each of the values in a separate row.
    """
    clean_edges=[]
    for i, row in tmp_edges_df.iterrows():
        if ',' in row[col]:
            vals=row[col].split(',')
            for v in vals:
                a_row=copy(row)
                a_row[col]=v
                clean_edges.append(a_row)
        else:
            clean_edges.append(row)
    return clean_edges

def extract_label_aliases(a_list):
    label=''
    aliases=''
    if len(a_list):
        label=a_list[0].replace('_', ' ')
        if len(a_list)>1:
            alias_labels=[]
            for l in a_list[1:]:
                if l!=a_list[0]:
                    alias_labels.append(l.replace('_', ' '))
            aliases=','.join(alias_labels)
    return label, aliases

def add_lowercase_labels(labels):
    """
    Transform the list of labels into label and aliases, but also add lowercase label versions.
    """
    label, *aliases=list(labels)
    added=set()
    for lbl in labels:
        if not lbl.islower() and lbl.lower() not in labels:
            added.add(lbl.lower())

    aliases = list(set(aliases) | added)
    return label, aliases

def merge_clusters(node2cluster, s, o):
    for k, v in node2cluster.items():
        if v==o:
            node2cluster[v]=node2cluster[s]
    return node2cluster

def compute_sameas_replacements(edges_df):
    sameas_df=edges_df[edges_df['predicate']=='mw:SameAs']
    node2cluster={}
    new_cluster_id=1
    for i, row in sameas_df.iterrows():
        s=row['subject']
        o=row['object']
        if s not in node2cluster.keys() and o not in node2cluster.keys():
            node2cluster[s]=node2cluster[o]=new_cluster_id
            new_cluster_id+=1
        elif s not in node2cluster.keys():
            node2cluster[s]=node2cluster[o]
        elif o not in node2cluster.keys():
            node2cluster[o]=node2cluster[s]
        else: # both are in a cluster
            if node2cluster[s]!=node2cluster[o]:
                node2cluster=merge_clusters(node2cluster, s, o)

    cid2members=defaultdict(set)
    for n, c in node2cluster.items():
        cid2members[c].add(n)

    names={}
    for c, nodes in cid2members.items():
        names[c]='+'.join(list(nodes))

    replacements={}
    for node, cid in node2cluster.items():
        replacements[node]=names[cid]
    return replacements

def replace_edges(edges_file, replacements, rep_nodes):
    new_rows=[]
    with open(edges_file, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for i, row in enumerate(spamreader):
            if row[0] in rep_nodes:
                row[0]=replacements[row[0]]
            if row[2] in rep_nodes:
                row[2]=replacements[row[2]]
            new_rows.append(row)
            if i%1000000==0:
                print(i, 'processed edges')
    return new_rows

def replace_nodes(nodes_file, replacements, rep_nodes):
    new_node_rows=[]
    with open(nodes_file, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for i, row in enumerate(spamreader):
            if row[0] in rep_nodes:
                row[0]=replacements[row[0]]
            new_node_rows.append(row)
    return new_node_rows

def collapse_identical_nodes(edges_file, nodes_file):

    edges_df=pd.read_csv(edges_file, sep='\t', header=0, na_filter= False)
    nodes_df=pd.read_csv(nodes_file, sep='\t', header=0, na_filter= False)

    print(len(edges_df))
    replacements=compute_sameas_replacements(edges_df)
    rep_nodes=set(replacements.keys())

    new_edge_rows=replace_edges(edges_file, replacements, rep_nodes)
    new_edges_df=pd.DataFrame(new_edge_rows, columns=edges_df.columns)
    new_edges_df=new_edges_df[new_edges_df['predicate']!='mw:SameAs']
    print(len(new_edges_df), 'edges')

    new_node_rows=replace_nodes(nodes_file, replacements, rep_nodes)
    new_nodes_df=pd.DataFrame(new_node_rows, columns=nodes_df.columns)
    node_transformations={'label': ','.join, 'aliases': ','.join, 'pos': ','.join, 'datasource': ','.join, 'other': list}
    new_nodes_df=deduplicate_with_transformations(new_nodes_df, 'id', node_transformations)


#    new_nodes_df.drop_duplicates(subset ="id",
#        keep = 'first', inplace = True)
    print(len(new_nodes_df), 'nodes')

    return new_edges_df, new_nodes_df
