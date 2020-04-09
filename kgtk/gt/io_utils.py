import argparse
import os
import csv
from tqdm import tqdm # type: ignore
import subprocess
import pandas as pd # type: ignore

from loguru import logger

def load_gt_graph(graph_path):
    """Load a graph in graphml or gt format."""
    from graph_tool.all import load_graph
    logger.info(f"loading the generated graph file from {graph_path}")
    g = load_graph(graph_path)
    return g

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def transform_to_graphtool_format(mowgli_nodes_path: str, mowgli_edges_path: str, graphml_path: str, do_gt: bool):
    n_nodes = file_len(mowgli_nodes_path)
    n_edges = file_len(mowgli_edges_path)

    logger.info(f'n_nodes: {n_nodes}, n_edges:{n_edges}')

    CHUNK = 100 * 1000

    graph_header = """<?xml version="1.0" encoding="UTF-8"?>
    <graphml xmlns="http://graphml.graphdrawing.org/xmlns"  
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
    http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">

    <key id="ndlabel" for="node" attr.name="label" attr.type="string"/>
    <key id="ndaliases" for="node" attr.name="aliases" attr.type="string"/>
    <key id="ndpos" for="node" attr.name="pos" attr.type="string"/>
    <key id="nddatasource" for="node" attr.name="datasource" attr.type="string"/>
    <key id="ndother" for="node" attr.name="other" attr.type="string"/>

    <key id="edpredicate" for="edge" attr.name="predicate" attr.type="string"/>
    <key id="eddatasource" for="edge" attr.name="datasource" attr.type="string"/>
    <key id="edweight" for="edge" attr.name="weight" attr.type="string"/>
    <key id="edother" for="edge" attr.name="other" attr.type="string"/>

    <graph id="G" edgedefault="directed">
    """

    graph_bottom = """</graph>
    </graphml>"""

    lut = str.maketrans({
        "\"": "&quot;",
        "\'": "&apos;",
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;"
    })

    def process_rows_iter(df_iter, max_len, output_file, func):
        total = 0.0
        last = False
        tbar = tqdm(total=100)
        step = round(float(CHUNK) / max_len * 100, 1)
        while not last:
            #         logger.info(f'Processed nodes {int((total/max_len)*100)}%')
            df = df_iter.get_chunk()

            total += CHUNK
            if len(df) < CHUNK:
                last = True
            (df.fillna('')
             .applymap(lambda s: str(s).translate(lut))
             .apply(func, axis=1)
             .to_csv(output_file, sep='\t', mode='a',
                     header=False, index=False,
                     quoting=csv.QUOTE_NONE, escapechar='\\'))
            tbar.update(step)

    logger.info('generating graphml format')
    with open(graphml_path, 'w') as fp:
        fp.write(graph_header)
        ###################################
        # write node info
        logger.info(f'Processing nodes info from {mowgli_nodes_path}')
        df_iter = pd.read_csv(
            mowgli_nodes_path, sep='\t', header=0,
            names=["id", "label", "aliases", "pos", 'datasource', 'other'],
            index_col=None, iterator=True, chunksize=CHUNK)

        def node_string(row):
            nid = row['id']
            attrs = "\t\n".join(
                [f'<data key=\'nd{k}\'>{v}</data>' for k, v in row.items() if k != 'id']
            )
            return f"<node id=\"{nid}\">\n{attrs}\n</node>"

        process_rows_iter(df_iter, n_nodes, output_file=fp, func=node_string)

        ###################################
        # write edge info
        logger.info(f'Processing edges info from {mowgli_edges_path}')
        df_iter = pd.read_csv(
            mowgli_edges_path, sep='\t', header=0,
            names=['subject', 'predicate', 'object', 'datasource', 'weight', 'other'],
            index_col=None, iterator=True, chunksize=CHUNK)

        def edge_string(row):
            subj = row['subject']
            obj = row['object']
            attrs = "\t\n".join(
                [f'<data key=\'ed{k}\'>{v}</data>'
                 for k, v in row.items() if k not in ['subject', 'object']]
            )
            return f"<edge source=\"{subj}\" target=\"{obj}\">\n{attrs}\n</edge>"

        process_rows_iter(df_iter, n_edges, output_file=fp, func=edge_string)

        ###################################
        fp.write(graph_bottom)

    if do_gt:
        g=load_gt_graph(graphml_path)
        gt_path = graphml_path.replace(".graphml", '.gt')
        logger.info(f'saving gt output at {gt_path}')
        g.save(gt_path)
    return g

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a machine commonsense dataset')
    parser.add_argument("--nodes", default="~/mowgli/mowgli_data/all/nodes_v002.csv",
                        help="path to mowgli nodes.csv file")
    parser.add_argument("--edges", default="~/mowgli/mowgli_data/all/edges_v002.csv",
                        help="path to mowgli edges.csv file")
    parser.add_argument("--output", default='~/mowgli/graph_data/all.graphml',
                        help="output graphml file")
    parser.add_argument("--gt", action="store_true",
                        help="whether to store to gt format too")

    args = parser.parse_args()
    logger.info(f'got: {args}')
    # mowgli_nodes_path = os.path.expanduser(f"~/mowgli/mowgli_data/{name}/nodes_v002.csv")
    # mowgli_edges_path = os.path.expanduser(f"~/mowgli/mowgli_data/{name}/edges_v002.csv")
    # graphml_path = os.path.expanduser(f'~/mowgli/graph_data/{name}.graphml')

    assert '.graphml' in args.output, f'output file must have \".graphml\" format. > {args.output} '

    g=transform_to_graphtool_format(mowgli_edges_path=args.edges, mowgli_nodes_path=args.nodes,
         graphml_path=args.output, do_gt=args.gt)
