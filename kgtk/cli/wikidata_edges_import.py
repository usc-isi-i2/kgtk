"""
Import wikidata edges into KGTK file
"""


def parser():
    return {
        'help': 'Import wikidata edges into KGTK file'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument("-i", action="store", type=str, dest="wikidata_file")
    parser.add_argument(
        "-e",
        action="store",
        type=str,
        dest="edge_file",
        default=None)
    parser.add_argument(
        "-q",
        action="store",
        type=str,
        dest="qual_file",
        default=None)
    parser.add_argument(
        "-l",
        action="store",
        type=int,
        dest="limit",
        default=None)
    parser.add_argument(
        "-L",
        action="store",
        type=str,
        dest="lang",
        default="en")
    parser.add_argument(
        "-s",
        action="store",
        type=str,
        dest="doc_id",
        default="wikidata-20200203")
    
    
def run(wikidata_file, edge_file, qual_file, limit, lang, doc_id):
    # import modules locally
    import bz2
    import json
    import csv
    
    site_filter = '{}wiki'.format(lang)

    WD_META_ITEMS = [
        "Q163875",
        "Q191780",
        "Q224414",
        "Q4167836",
        "Q4167410",
        "Q4663903",
        "Q11266439",
        "Q13406463",
        "Q15407973",
        "Q18616576",
        "Q19887878",
        "Q22808320",
        "Q23894233",
        "Q33120876",
        "Q42104522",
        "Q47460393",
        "Q64875536",
        "Q66480449",
    ]

    # filter: currently defined as OR: one hit suffices to be removed from
    # further processing
    exclude_list = WD_META_ITEMS

    # punctuation
    exclude_list.extend(["Q1383557", "Q10617810"])

    # letters etc
    exclude_list.extend(["Q188725", "Q19776628", "Q3841820",
                         "Q17907810", "Q9788", "Q9398093"])

    neg_prop_filter = {
        'P31': exclude_list,    # instance of
        'P279': exclude_list    # subclass
    }

    to_print = False
    # parse appropriate fields - depending on what we need in the KB
    parse_properties = True
    parse_qualifiers = True
    parse_claims = True
    write_edges = False
    write_qualifiers = False
    if edge_file is not None:
        write_edges = True
    if qual_file is not None:
        write_qualifiers = True
    # create the header of the csv file
    header = []
    header.append('id')
    header.append('node1')
    header.append('label')
    header.append('node2')
    header.append('magnitude')
    header.append('unit')
    header.append('lower')
    header.append('upper')
    header.append('latitude')
    header.append('longitude')
    header.append('precision')
    header.append('calendar')
    header.append('entity-type')
    # header.append('document_id')
    if write_edges:
        with open(edge_file, 'w', newline='') as myfile:
            wr = csv.writer(
                myfile,
                quoting=csv.QUOTE_NONE,
                delimiter="\t",
                escapechar="\n",
                quotechar='')
            wr.writerow(header)
    if write_qualifiers:
        header.append('short_node1_id')
        with open(qual_file, 'w', newline='') as myfile:
            wr = csv.writer(
                myfile,
                quoting=csv.QUOTE_NONE,
                delimiter="\t",
                escapechar="\n",
                quotechar='')
            wr.writerow(header)
    rows = []
    qrows = []
    short_id = 1
    with bz2.open(wikidata_file, mode='rb') as file:
        print('processing wikidata file now...')
        for cnt, line in enumerate(file):
            if limit and cnt >= limit:
                break
            if cnt % 500000 == 0 and cnt > 0:
                #logger.info("processed {} lines of WikiData JSON dump".format(cnt))
                print('processed {} lines'.format(cnt))
            clean_line = line.strip()
            if clean_line.endswith(b","):
                clean_line = clean_line[:-1]
            if len(clean_line) > 1:
                obj = json.loads(clean_line)
                entry_type = obj["type"]
                if entry_type == "item" or entry_type == "property":
                    keep = True

                claims = obj["claims"]

                if parse_claims:
                    for prop, value_set in neg_prop_filter.items():
                        claim_property = claims.get(prop, None)
                        if claim_property:
                            for cp in claim_property:
                                cp_id = (
                                    cp["mainsnak"]
                                    .get("datavalue", {})
                                    .get("value", {})
                                    .get("id")
                                )
                                cp_rank = cp["rank"]
                                if cp_rank != "deprecated" and cp_id in value_set:
                                    keep = False

                if keep:
                    qnode = obj["id"]
                    if parse_properties:
                        for prop, claim_property in claims.items():
                            # cp_vals=[]
                            seq_no = 1
                            for cp in claim_property:
                                if cp['rank'] != 'deprecated' and cp['mainsnak']['snaktype'] == 'value':
                                    val = cp['mainsnak']['datavalue'].get(
                                        'value')
                                    typ = cp['mainsnak']['datatype']
                                    sid = qnode + '-' + \
                                        prop + '-' + str(seq_no)
                                    short_sid = '__' + str(short_id)
                                    value = ''
                                    mag = ''
                                    unit = ''
                                    lower = ''
                                    upper = ''
                                    precision = ''
                                    calendar = ''
                                    lat = ''
                                    long = ''
                                    enttype = ''
                                    short_id += 1
                                    if typ.startswith('wikibase'):
                                        enttype = val.get('entity-type')
                                        value = val.get('id', '')
                                    elif typ == 'quantity':
                                        value = val['amount']
                                        mag = val['amount']
                                        if val.get(
                                                'upperBound',
                                                None) or val.get(
                                                'lowerBound',
                                                None):
                                            lower = val.get('lowerBound', '')
                                            upper = val.get('upperBound', '')
                                            value += '[' + lower + \
                                                ',' + upper + ']'
                                        if len(val.get('unit')) > 1:
                                            unit = val.get(
                                                'unit').split('/')[-1]
                                            value += unit
                                    elif typ == 'globe-coordinate':
                                        lat = str(val['latitude'])
                                        long = str(val['longitude'])
                                        precision = val.get('precision', '')
                                        value = '@' + lat + '/' + long
                                    elif typ == 'time':
                                        mag = "^" + val['time'][1:]
                                        precision = str(val['precision'])
                                        calendar = val.get(
                                            'calendarmodel', '').split('/')[-1]
                                        value = "^" + \
                                            val['time'][1:] + '/' + str(val['precision'])
                                    elif typ == 'monolingualtext':
                                        value = '\'' + \
                                            val['text'] + '\'' + '@' + val['language']
                                    else:
                                        value = '\"' + val + '\"'
                                    if write_edges:
                                        rows.append([short_sid,
                                                     qnode,
                                                     prop,
                                                     value,
                                                     mag,
                                                     unit,
                                                     lower,
                                                     upper,
                                                     lat,
                                                     long,
                                                     precision,
                                                     calendar,
                                                     enttype])
                                    # add an edge from the item to the statement with prefix 'ps:' for the property
                                    # prop_name='ps:'+prop
                                    # statement_id=qnode+'-'+prop_name+'-'+str(seq_no)
                                    # rows.append([statement_id,qnode,prop_name,sid,doc_id])
                                    seq_no += 1
                                    # get qualifiers for the statements that we
                                    # are importing
                                    if parse_qualifiers:
                                        if cp.get('qualifiers', None):
                                            quals = cp['qualifiers']
                                            for qual_prop, qual_claim_property in quals.items():
                                                qual_seq_no = 1
                                                for qcp in qual_claim_property:
                                                    if qcp['snaktype'] == 'value':
                                                        value = ''
                                                        mag = ''
                                                        unit = ''
                                                        lower = ''
                                                        upper = ''
                                                        precision = ''
                                                        calendar = ''
                                                        lat = ''
                                                        long = ''
                                                        enttype = ''
                                                        val = qcp['datavalue'].get(
                                                            'value')
                                                        typ = qcp['datatype']
                                                        tempid = sid + '-' + qual_prop + \
                                                            '-' + str(qual_seq_no)
                                                        qual_seq_no += 1
                                                        if typ.startswith(
                                                                'wikibase'):
                                                            enttype = val.get(
                                                                'entity-type')
                                                            value = val.get(
                                                                'id', '')
                                                        elif typ == 'quantity':
                                                            value = val['amount']
                                                            mag = val['amount']
                                                            if val.get(
                                                                    'upperBound',
                                                                    None) or val.get(
                                                                    'lowerBound',
                                                                    None):
                                                                lower = val.get(
                                                                    'lowerBound', '')
                                                                upper = val.get(
                                                                    'upperBound', '')
                                                                value += '[' + lower + \
                                                                    ',' + upper + ']'
                                                            if len(
                                                                    val.get('unit')) > 1:
                                                                unit = val.get(
                                                                    'unit').split('/')[-1]
                                                                value += unit
                                                        elif typ == 'globe-coordinate':
                                                            lat = str(
                                                                val['latitude'])
                                                            long = str(
                                                                val['longitude'])
                                                            precision = val.get(
                                                                'precision', '')
                                                            value = '@' + lat + '/' + long
                                                        elif typ == 'time':
                                                            mag = "^" + \
                                                                val['time'][1:]
                                                            precision = str(
                                                                val['precision'])
                                                            calendar = val.get(
                                                                'calendarmodel', '').split('/')[-1]
                                                            value = "^" + \
                                                                val['time'][1:] + '/' + str(val['precision'])
                                                        elif typ == 'monolingualtext':
                                                            value = '\'' + \
                                                                val['text'] + '\'' + '@' + val['language']
                                                        else:
                                                            value = '\"' + val + '\"'
                                                        if write_qualifiers:
                                                            qrows.append(
                                                                [
                                                                    tempid,
                                                                    sid,
                                                                    qual_prop,
                                                                    value,
                                                                    mag,
                                                                    unit,
                                                                    lower,
                                                                    upper,
                                                                    lat,
                                                                    long,
                                                                    precision,
                                                                    calendar,
                                                                    enttype,
                                                                    short_sid])
            if cnt % 50000 == 0 and cnt > 0:
                if write_edges:
                    with open(edge_file, 'a', newline='') as myfile:
                        for row in rows:
                            wr = csv.writer(
                                myfile,
                                quoting=csv.QUOTE_NONE,
                                delimiter="\t",
                                escapechar="\n",
                                quotechar='')
                            wr.writerow(row)
                        rows = []
                if write_qualifiers:
                    with open(qual_file, 'a', newline='') as myfile:
                        for row in qrows:
                            wr = csv.writer(
                                myfile,
                                quoting=csv.QUOTE_NONE,
                                delimiter="\t",
                                escapechar="\n",
                                quotechar='')
                            wr.writerow(row)
                        qrows = []
                        myfile.close()
    if write_edges:
        with open(edge_file, 'a', newline='') as myfile:
            for row in rows:
                wr = csv.writer(
                    myfile,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='')
                wr.writerow(row)
    if write_qualifiers:
        with open(qual_file, 'a', newline='') as myfile:
            for row in qrows:
                wr = csv.writer(
                    myfile,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='')
                wr.writerow(row)
    print('import complete')
