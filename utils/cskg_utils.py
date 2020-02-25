import pandas as pd

def append_df_with_missing_nodes(base_df, missing_nodes, datasource, node_columns):
    print(missing_nodes)
    rows=[]
    for n in missing_nodes:
        a_row=[n, "", "", "", datasource, {}]
        rows.append(a_row)
    new_df=pd.DataFrame(rows, columns=node_columns)
    combined_nodes = pd.concat([base_df, new_df])
    print(len(combined_nodes), 'nodes')

    return combined_nodes

