import pandas as pd

##########################################
#    Obtain data functions
##########################################

def get_float_year(input):
    date = input[1:input.find('T')]
    ymd = date.split('-')
    return float(ymd[0]) + float(ymd[1])/12 + float(ymd[2])/12/12

def get_data_only(entity_path):

    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    entities = pd.DataFrame(columns=['node1', 'label', 'node2'])

    kr_ent: KgtkReader = KgtkReader.open(entity_path)

    for row in kr_ent:
        if row[kr_ent.column_name_map['node2']].startswith('^'):
            entities.loc[len(entities.index)] = {'node1': row[kr_ent.column_name_map['node1']],
                                                 'label': row[kr_ent.column_name_map['label']],
                                                 'node2': get_float_year(row[kr_ent.column_name_map['node2']])}
        else:
            entities.loc[len(entities.index)] = {'node1': row[kr_ent.column_name_map['node1']],
                                                 'label': row[kr_ent.column_name_map['label']],
                                                 'node2': row[kr_ent.column_name_map['node2']]}


    return entities

def get_data_lp(dataset, train_file_path, num_literal_path):
    """
    Get the entity file and literal file for Link Prediction
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    entities = pd.DataFrame(columns=['node1', 'label', 'node2'])
    df = pd.DataFrame(columns=['node1', 'label', 'node2'])

    kr_train: KgtkReader = KgtkReader.open(f"{dataset}/{train_file_path}")

    for row in kr_train:
        entities.loc[len(entities.index)] = {'node1': row[kr_train.column_name_map['node1']],
                                             'label': row[kr_train.column_name_map['label']],
                                             'node2': row[kr_train.column_name_map['node2']]}

    kr_train.close()

    kr_num: KgtkReader = KgtkReader.open(f"{dataset}/{num_literal_path}")

    for row in kr_num:
        df.loc[len(df.index)] = {'node1': row[kr_num.column_name_map['node1']],
                                             'label': row[kr_num.column_name_map['label']],
                                             'node2': row[kr_num.column_name_map['node2']]}
    kr_num.close()

    df = df[df['node2'].notnull()]
    df = df.reset_index(drop=True)

    return entities, df


def clean_entities(df, dataset):
    if dataset.lower() == "yago15k":
        df[0] = df[0].apply(lambda x: x.split("resource")[-1][1:-1])
        df[1] = df[1].apply(lambda x: x.split("resource")[-1][1:-1])
        df[2] = df[2].apply(lambda x: x.split("resource")[-1][1:-1])
    df.columns = ['node1', 'label', 'node2']
    return df


def clean_numeric(df, dataset):
    if dataset.lower() == "yago15k":
        df[0] = df[0].apply(lambda x: x.split("resource")[-1][1:-1])
        df[1] = df[1].apply(lambda x: x.split("resource")[-1][1:-1])
    elif dataset.lower() == "fb15k237":
        df[1] = df[1].apply(lambda x: x.split("ns")[-1][1:-1])
    df.columns = ['node1', 'label', 'node2']
    df = df[df['node2'].notnull()]
    df = df.reset_index(drop=True)
    return df


def get_data_np(dataset, entity_triple_name, train_literal_name,
                         valid_literal_name, test_literal_name):
    """ Get the entity file and literal file for """

    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    entities = pd.DataFrame(columns=['node1', 'label', 'node2'])
    train = pd.DataFrame(columns=['node1', 'label', 'node2'])
    valid = pd.DataFrame(columns=['node1', 'label', 'node2'])
    test = pd.DataFrame(columns=['node1', 'label', 'node2'])

    kr_entities: KgtkReader = KgtkReader.open(f"{dataset}/{entity_triple_name}")
    kr_train: KgtkReader = KgtkReader.open(f"{dataset}/{train_literal_name}")
    kr_valid: KgtkReader = KgtkReader.open(f"{dataset}/{valid_literal_name}")
    kr_test: KgtkReader = KgtkReader.open(f"{dataset}/{test_literal_name}")



    for row in kr_entities:
        entities.loc[len(entities.index)] = {'node1': row[kr_entities.column_name_map['node1']],
                                             'label': row[kr_entities.column_name_map['label']],
                                             'node2': row[kr_entities.column_name_map['node2']]}

    for row in kr_train:
        train.loc[len(train.index)] = {'node1': row[kr_train.column_name_map['node1']],
                                       'label': row[kr_train.column_name_map['label']],
                                       'node2': row[kr_train.column_name_map['node2']]}

    for row in kr_valid:
        valid.loc[len(valid.index)] = {'node1': row[kr_valid.column_name_map['node1']],
                                       'label': row[kr_valid.column_name_map['label']],
                                       'node2': row[kr_valid.column_name_map['node2']]}
    for row in kr_test:
        test.loc[len(test.index)] = {'node1': row[kr_test.column_name_map['node1']],
                                     'label': row[kr_test.column_name_map['label']],
                                     'node2': row[kr_test.column_name_map['node2']]}


    entities = entities[entities['node2'].notnull()]
    entities = entities.reset_index(drop=True)

    train = train[train['node2'].notnull()]
    train = train.reset_index(drop=True)

    valid = valid[valid['node2'].notnull()]
    valid = valid.reset_index(drop=True)

    test = test[test['node2'].notnull()]
    test = test.reset_index(drop=True)

    kr_entities.close()
    kr_train.close()
    kr_valid.close()
    kr_test.close()


    return entities, train, valid, test
