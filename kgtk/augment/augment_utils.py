import pandas as pd
from tqdm import tqdm
from bisect import bisect
from kgtk.augment.utils import *
from kgtk.augment.loader import *
from kgtk.augment.partition import *




##########################################
#    Edge Generation Utility Functions
##########################################



def get_edge_starts(df_sli, mode, num_bins=None):
    """
    Get the start of each bin
    """
    if mode.startswith('Quantile'):
        bins = get_bins_quantile(df_sli, num_bins)
    elif mode.startswith('Fixed'):
        bins = get_bins_fixed_length(df_sli, num_bins)
    elif mode.startswith('Jenks'):
        bins = get_bins_jenks(df_sli)
    elif mode.startswith('Kde'):
        bins = get_bins_kde(df_sli)
    else:  # Unsupported Mode
        return None
    return bins


def create_chain(qnodes_collect, property_, reverse_chain=True):
    """
    create the chain needed
    """
    qnode_chain = []
    for i in range(len(qnodes_collect)):
        if reverse_chain and i > 0:
            qnode_chain.append({
                'node1': qnodes_collect[i],
                'label': property_ + '_prev',
                'node2': qnodes_collect[i - 1]
            })
        if i < len(qnodes_collect) - 1:
            qnode_chain.append({
                'node1': qnodes_collect[i],
                'label': property_ + '_next',
                'node2': qnodes_collect[i + 1]
            })
    return qnode_chain


def create_hierarchy(qnodes_collect_a, qnodes_collect_b, property_, reverse_relation=True):
    """
    create the hierarchy needed
    """
    qnode_hierarchy = []
    for i in range(len(qnodes_collect_a)):
        qnode_hierarchy.append({
            'node1': qnodes_collect_a[i],
            'label': property_ + '_is_subgroup_of',
            'node2': qnodes_collect_b[i // 2]
        })
        if reverse_relation:
            qnode_hierarchy.append({
                'node1': qnodes_collect_b[i // 2],
                'label': property_ + '_has_subgroup',
                'node2': qnodes_collect_a[i]
            })
    return qnode_hierarchy


def create_literal_labels(bins, property_):
    """
    Create labels for quantity_intervals
    """
    qnodes_collect = []
    qnodes_label_edges = []

    for i in range(len(bins)):
        if i == 0:
            start = float(bins[i])
        else:
            start = float(bins[i]) + 1e-6

        if i == len(bins) - 1:
            end = 'inf'
        else:
            end = float(bins[i + 1])

        _qnode = gen_qnode(property_, start, end)
        _qlabel = gen_qlabel(property_, start, end)

        qnodes_collect.append(_qnode)

        qnodes_label_edges.append({
            'node1': _qnode,
            'label': 'label',
            'node2': _qlabel
        })
    return qnodes_collect, qnodes_label_edges


def create_property_labels(property_, unit):
    """ Generate the pnodes """
    pnodes_collect = []
    pnodes_edges = []
    pnodes_label_edges = []

    _pnode = gen_pnode(property_, unit)
    pnodes_collect.append(_pnode)
    _plabel = gen_plabel(property_, unit)
    pnodes_label_edges.append({
        'node1': _pnode,
        'label': 'label',
        'node2': _plabel
    })
    return pnodes_collect, pnodes_edges, pnodes_label_edges


def create_numeric_edges(df_sli, bins, qnodes_collect, suffix=""):
    """ Create numeric edges """
    numeric_edges = []
    if len(qnodes_collect) == 0:
        return numeric_edges

    for i, row in df_sli.iterrows():
        _pnode = gen_pnode(row['label'])
        try:
            _qnode = qnodes_collect[bisect(bins, row['node2']) - 1]
        except:
            _qnode = qnodes_collect[0]
        numeric_edges.append({
            'node1': row['node1'],
            'label': f"{_pnode}{suffix}",
            'node2': _qnode
        })
    return numeric_edges


##########################################
#    Edge Generation Functions
##########################################

def generate_edges_single(train, property_, num_bins=None, unit=None, mode='Quantile_Single',
                          valid=None, test=None, reverse=False):
    """
    Generate a 1D partition of literal nodes and add them to entity nodes
    """
    bins = get_edge_starts(train, mode, num_bins)
    # Generate the qnode
    qnodes_collect, qnodes_label_edges = create_literal_labels(bins, property_)

    # Connect with quantity nodes
    qnode_chain = create_chain(qnodes_collect, property_, reverse_chain=reverse)
    # Generate the pnodes
    pnodes_collect, pnodes_edges, pnodes_label_edges = create_property_labels(property_, unit)
    # Generate numeric edges
    numeric_edges_train = create_numeric_edges(train, bins, qnodes_collect)
    numeric_edges_valid = create_numeric_edges(valid, bins, qnodes_collect) if valid is not None else None
    numeric_edges_test = create_numeric_edges(test, bins, qnodes_collect) if test is not None else None

    return qnode_chain, qnodes_label_edges, pnodes_edges, pnodes_label_edges, \
        (numeric_edges_train, numeric_edges_valid, numeric_edges_test)


def generate_edges_overlapping(train, property_, num_bins=None, unit=None, mode='Quantile_Overlap',
                               valid=None, test=None, reverse=False):
    def compute_numeric_edges(df, bins_a, bins_b, qnodes_collect_a, qnodes_collect_b):
        if df is None:
            return None
        numeric_edges_a = create_numeric_edges(df, bins_a, qnodes_collect_a, suffix="_right")
        numeric_edges_b = create_numeric_edges(df, bins_b, qnodes_collect_b, suffix="_left")
        numeric_edges = numeric_edges_a + numeric_edges_b
        return numeric_edges

    """
    One numeric edge = 2 links
    """
    bs = get_edge_starts(train, mode, num_bins)
    bins_a, bins_b = bs[0::2], np.concatenate(([bs[0]], bs[1::2]))

    qnodes_collect_a, qnodes_label_edges_a = create_literal_labels(bins_a, property_)
    qnodes_collect_b, qnodes_label_edges_b = create_literal_labels(bins_b, property_)
    qnodes_label_edges = qnodes_label_edges_a + qnodes_label_edges_b

    qnodes_collect_all = []
    for i in range(len(qnodes_collect_a)):
        qnodes_collect_all.append(qnodes_collect_a[i])
        qnodes_collect_all.append(qnodes_collect_b[i])
    if len(qnodes_collect_a) > len(qnodes_collect_b):
        qnodes_collect_all += qnodes_collect_a[len(qnodes_collect_b):]

    qnode_chain = create_chain(qnodes_collect_all, property_, reverse_chain=reverse)

    pnodes_collect, pnodes_edges, pnodes_label_edges = create_property_labels(property_, unit)

    numeric_edges_train = compute_numeric_edges(train, bins_a, bins_b, qnodes_collect_a, qnodes_collect_b)
    numeric_edges_valid = compute_numeric_edges(valid, bins_a, bins_b, qnodes_collect_a, qnodes_collect_b)
    numeric_edges_test = compute_numeric_edges(test, bins_a, bins_b, qnodes_collect_a, qnodes_collect_b)

    return qnode_chain, qnodes_label_edges, pnodes_edges, pnodes_label_edges, \
        (numeric_edges_train, numeric_edges_valid, numeric_edges_test)


def generate_edges_hierarchy(train, property_, levels=3, unit=None, mode='Quantile_Hierarchy',
                             valid=None, test=None, reverse=False):
    """
    Link Hierarchy
    """
    from functools import reduce
    def compute_numeric_edges(df, bs_list, qnodes_collect_list):
        if df is None:
            return None
        numeric_edges_list = list()
        for lv in range(levels + 1):
            numeric_edges_list.append(
                create_numeric_edges(train, bs_list[lv], qnodes_collect_list[lv], suffix=f"_{lv}")
            )
        return reduce(lambda x, y: x + y, numeric_edges_list)

    bs = get_edge_starts(train, mode, 2 ** levels)
    bs_list = []
    for lv in range(levels + 1):
        bs_list.append(bs[0::2 ** lv])

    qnodes_collect_list, qnodes_label_edges_list = list(), list()
    for lv in range(levels + 1):
        _a, _b = create_literal_labels(bs_list[lv], property_)
        qnodes_collect_list.append(_a)
        qnodes_label_edges_list.append(_b)

    qnode_chain_list = list()
    for lv in range(levels + 1):
        qnode_chain_list.append(create_chain(qnodes_collect_list[lv], property_, reverse_chain=reverse))
    for lv in range(levels - 1):
        qnode_chain_list.append(create_hierarchy(qnodes_collect_list[lv], qnodes_collect_list[lv + 1],
                                                 property_, reverse_relation=reverse))

    pnodes_collect, pnodes_edges, pnodes_label_edges = create_property_labels(property_, unit)

    qnode_chain = reduce(lambda x, y: x + y, qnode_chain_list)
    qnodes_label_edges = reduce(lambda x, y: x + y, qnodes_label_edges_list)
    numeric_edges_train = compute_numeric_edges(train, bs_list, qnodes_collect_list)
    numeric_edges_valid = compute_numeric_edges(valid, bs_list, qnodes_collect_list)
    numeric_edges_test = compute_numeric_edges(test, bs_list, qnodes_collect_list)

    return qnode_chain, qnodes_label_edges, pnodes_edges, pnodes_label_edges, \
        (numeric_edges_train, numeric_edges_valid, numeric_edges_test)


##########################################
#    Edge Creation Functions
##########################################

#usage create_new_edges(train, mode, bins, valid=valid, test=test, reverse=reverse)

def create_new_edges(train, mode, num_bins=None, valid=None, test=None, reverse=False):
    """
    Create the new edges based on the partitioned data
    """

    qnodes_edges, qnodes_label_edges = [], []  # (metadata) entity labels
    pnodes_edges, pnodes_label_edges = [], []  # (metadata) property labels
    train_edges, train_edges_raw = [], None  # numeric edges (node2 as numbers)
    valid_edges, valid_edges_raw = [], None
    test_edges, test_edges_raw = [], None

    for property_ in tqdm(train['label'].unique()):

        # Iterate through each numeric property
        sli_train = train[train['label'] == property_]
        if len(sli_train) < 100:  # Filter out rare properties
            continue
        sli_valid = valid[valid['label'] == property_] if valid is not None else None
        sli_test = test[test['label'] == property_] if test is not None else None

        try:
            if mode.endswith("Single"):
                assert(num_bins is not None)
                a, b, c, d, e = generate_edges_single(sli_train, property_, num_bins=num_bins,
                                                      unit=None, mode=mode, valid=sli_valid, test=sli_test,
                                                      reverse=reverse)
            elif mode.endswith("Overlap"):
                assert(num_bins is not None)
                a, b, c, d, e = generate_edges_overlapping(sli_train, property_, num_bins=num_bins,
                                                           unit=None, mode=mode, valid=sli_valid, test=sli_test,
                                                           reverse=reverse)
            elif mode.endswith("Hierarchy"):
                assert(num_bins is not None)
                a, b, c, d, e = generate_edges_hierarchy(sli_train, property_, levels=int(np.log2(num_bins)),
                                                         unit=None, mode=mode, valid=sli_valid, test=sli_test,
                                                         reverse=reverse)
            else:
                print("Unsupported data type!")
                continue



            qnodes_edges += a
            qnodes_label_edges += b
            pnodes_edges += c
            pnodes_label_edges += d

            train_edges += e[0]
            train_edges_raw = sli_train if train_edges_raw is None else pd.concat([train_edges_raw, sli_train])

            if valid is not None:
                valid_edges += e[1]
                valid_edges_raw = sli_valid if valid_edges_raw is None else pd.concat([valid_edges_raw, sli_valid])
            if test is not None:
                test_edges += e[2]
                test_edges_raw = sli_test if test_edges_raw is None else pd.concat([test_edges_raw, sli_test])


        except TypeError as e:
            assert(sli_train is not None)
            print(f"Error encountered at property {property_}. Size {len(sli_train)}. Error: {e}. Continue...")
            import traceback
            traceback.print_exc()

    train_edges_processed = pd.DataFrame(train_edges)
    if valid is None or test is None:
        return (train_edges_processed, None, None), (train_edges_raw, None, None), qnodes_edges
    valid_edges_processed = pd.DataFrame(valid_edges)
    test_edges_processed = pd.DataFrame(test_edges)
    return (train_edges_processed, valid_edges_processed, test_edges_processed), \
           (train_edges_raw, valid_edges_raw, test_edges_raw), qnodes_edges
