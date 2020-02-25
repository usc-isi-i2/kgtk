import pandas as pd
from copy import copy

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
