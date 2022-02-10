from kgtk.augment.constant import *
from kgtk.augment.augment_utils import *
from collections import defaultdict
import os
import json
import shutil
from kgtk.io.kgtkwriter import KgtkWriter


def try_to_make_dir(folder):
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass


def kgtk_writer_to_file(df, output_path):
    df = df.reset_index(drop=True)
    kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2"],
                                     output_path
                                     )
    for i in range(0, len(df)):
        kw.write([str(df['node1'][i]), str(df['label'][i]), str(df['node2'][i])])

    kw.close()

##########################################
#    Main Function
##########################################


def augment_lp(entities, df, dataset, train_file_path ,valid_file_path,
               test_file_path, mode, output_path, bins=None, reverse=False):
    suffix = int(np.log2(bins)) if mode.endswith("Hierarchy") else bins

    if mode in CHAINABLE_MODE:
        print(f'Running mode {mode}')

        (numeric_edges_processed, _, _), _, qnode_edges = create_new_edges(df, mode, bins, reverse=reverse)

        if dataset is None:
            folder = 'augment_output'
        else:
            folder = dataset.split('/')[-1]

        # Write the augmented version (without chain)
        target = f'{output_path}/{folder}_{mapping_no_chain[mode]}_{suffix}'
        if reverse:
            target += "_reverse"
        try_to_make_dir(target)

        kgtk_writer_to_file(pd.concat([entities, numeric_edges_processed]), f'{target}/{train_file_path}')
        shutil.copy(f'{dataset}/{valid_file_path}', f'{target}/{valid_file_path}')
        shutil.copy(f'{dataset}/{test_file_path}', f'{target}/{test_file_path}')

        # Write the augmented version (with chain)
        target = f'{output_path}/{folder}_{mapping_chain[mode]}_{suffix}'
        if reverse:
            target += "_reverse"
        try_to_make_dir(target)

        kgtk_writer_to_file(pd.concat([entities, numeric_edges_processed,
                                       pd.DataFrame(qnode_edges)]), f'{target}/{train_file_path}')
        shutil.copy(f'{dataset}/{valid_file_path}', f'{target}/{valid_file_path}')
        shutil.copy(f'{dataset}/{test_file_path}', f'{target}/{test_file_path}')


def augment_np(entities, train, valid, test, entity_triple_name, train_literal_name,
               valid_literal_name, test_literal_name, dataset, mode, output_path, bins=None, reverse=False):
    suffix = int(np.log2(bins)) if mode.endswith("Hierarchy") else bins

    if mode in CHAINABLE_MODE:

        print(f'Running mode {mode}')

        (train_edges_processed, valid_edges_processed, test_edges_processed), \
            (train_edges_raw, valid_edges_raw, test_edges_raw), qnode_edges = \
            create_new_edges(train, mode, bins, valid=valid, test=test, reverse=reverse)

        return 0

        medians_dict = {}
        collections = defaultdict(list)
        collections_raw = defaultdict(list)

        if train_edges_raw is not None:
            for i, row in train_edges_raw.iterrows():
                collections_raw[row['node1'] + '  ' + row['label']].append(row['node2'])

        if len(train_edges_processed) == 0:
            print('no edges')

        if len(train_edges_processed) > 0:
            for i, row in train_edges_processed.iterrows():
                key = row['node1'] + '  ' + row['label'].split('-')[1].rsplit('_', 1)[0]
                for item in collections_raw[key]:
                    collections[row['node2']].append(item)

        for k, v in collections.items():
            medians_dict[k] = np.median([float(item) for item in v])

        # Finally, add the median of each property as a baseline
        if train_edges_raw is not None:
            for property_ in train_edges_raw['label'].unique():
                medians_dict[property_] = \
                    train_edges_raw[train_edges_raw['label'] == property_]['node2'].median()

        # Write the original version
        def generate_target(target, with_chain=False):
            try_to_make_dir(target)
            if not with_chain:
                kgtk_writer_to_file(pd.concat([entities, train_edges_processed]), f'{target}/train.tsv')
            else:
                kgtk_writer_to_file(pd.concat([entities, train_edges_processed,
                                               pd.DataFrame(qnode_edges)]), f'{target}/train.tsv')

            kgtk_writer_to_file(valid_edges_processed, f'{target}/valid.tsv')
            kgtk_writer_to_file(test_edges_processed, f'{target}/test.tsv')
            kgtk_writer_to_file(valid_edges_raw, f'{target}/valid_raw.tsv')
            kgtk_writer_to_file(valid_edges_processed, f'{target}/test_raw.tsv')

            with open(f'{target}/medians.dict', 'w+') as fd:
                json.dump(medians_dict, fd, indent=2)

        if dataset is None:
            folder = 'augment_output'
        else:
            folder = dataset.split('/')[-1]

        target = f'{output_path}/{folder}_{mapping_no_chain[mode]}_{suffix}'
        if reverse:
            target += "_reverse"
        generate_target(target)

        target = f'{output_path}/{folder}_{mapping_chain[mode]}_{suffix}'
        if reverse:
            target += "_reverse"
        generate_target(target, with_chain=True)


def augment_only(entities, dataset, mode, output_path, bins=None, reverse=False, include_original=True):
    suffix = int(np.log2(bins)) if mode.endswith("Hierarchy") else bins

    if dataset is None:
        folder = 'augment_output'
    else:
        folder = dataset.split('/')[-1]

    if mode in CHAINABLE_MODE:
        print(f'Running mode {mode}')

        (train_edges_processed, valid_edges_processed, test_edges_processed), \
        (train_edges_raw, valid_edges_raw, test_edges_raw), qnode_edges = \
        create_new_edges(entities, mode, bins, valid=None, test=None, reverse=reverse)

        def generate_target(target, with_chain=False, include_original=True):
            try_to_make_dir(target)
            if not with_chain:
               if include_original:
                    kgtk_writer_to_file(train_edges_processed, f'{target}/output.tsv')
                else:
                    kgtk_writer_to_file(pd.concat([entities, train_edges_processed]), f'{target}/output.tsv')
            else:
                if include_original:
                    kgtk_writer_to_file(pd.concat([train_edges_processed,
                                                   pd.DataFrame(qnode_edges)]), f'{target}/output.tsv')
                else:
                    kgtk_writer_to_file(pd.concat([entities, train_edges_processed,
                                                   pd.DataFrame(qnode_edges)]), f'{target}/output.tsv')

        target = f'{output_path}/{folder}_{mapping_no_chain[mode]}_{suffix}'
        if reverse:
            target += "_reverse"
        generate_target(target, with_chain=False, include_original=include_original)

        target = f'{output_path}/{folder}_{mapping_chain[mode]}_{suffix}'
        if reverse:
            target += "_reverse"
        generate_target(target, with_chain=True, include_original=include_original)
