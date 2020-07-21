"""
Import an wikidata file into KGTK file
"""

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import an wikidata file into KGTK file'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.utils.argparsehelpers import optional_bool
    
    parser.add_input_file(positional=True, who='input path file (may be .bz2)')

    parser.add_argument(
        '--procs',
        action="store",
        type=int,
        dest="procs",
        default=2,
        help='number of processes to run in parallel, default 2')
    parser.add_argument(
        "--node",
        action="store",
        type=str,
        dest="node_file",
        default=None,
        help='path to output node file')
    parser.add_argument(
        "--edge",
        action="store",
        type=str,
        dest="edge_file",
        default=None,
        help='path to output edge file')
    parser.add_argument(
        "--qual",
        action="store",
        type=str,
        dest="qual_file",
        default=None,
        help='path to output qualifier file')
    parser.add_argument(
        "--limit",
        action="store",
        type=int,
        dest="limit",
        default=None,
        help='number of lines of input file to run on, default runs on all')
    parser.add_argument(
        "--lang",
        action="store",
        type=str,
        dest="lang",
        default="en",
        help='languages to extract, comma separated, default en')
    parser.add_argument(
        "--source",
        action="store",
        type=str,
        dest="source",
        default="wikidata",
        help='wikidata version number, default: wikidata')
    parser.add_argument(
        "--deprecated",
        action="store_true",
        dest="deprecated",
        help='option to include deprecated statements, not included by default')
    
    parser.add_argument(
        "--explode-values",
        nargs='?',
        type=optional_bool,
        dest="explode_values",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create columns with exploded value information. (default=%(default)s).",
    )

    parser.add_argument(
        "--use-python-cat",
        nargs='?',
        type=optional_bool,
        dest="use_python_cat",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use portable code to combine file fragments. (default=%(default)s).",
    )

    parser.add_argument(
        "--keep-temp-files",
        nargs='?',
        type=optional_bool,
        dest="keep_temp_files",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, keep temporary files (for debugging). (default=%(default)s).",
    )

    parser.add_argument(
        "--skip-processing",
        nargs='?',
        type=optional_bool,
        dest="skip_processing",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, skip processing the input file (for debugging). (default=%(default)s).",
    )

    parser.add_argument(
        "--skip-merging",
        nargs='?',
        type=optional_bool,
        dest="skip_merging",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, skip merging temporary files (for debugging). (default=%(default)s).",
    )

    
def run(input_file: KGTKFiles,
        procs,
        node_file,
        edge_file,
        qual_file,
        limit,
        lang,
        source,
        deprecated,
        explode_values,
        use_python_cat,
        keep_temp_files,
        skip_processing,
        skip_merging):
    # import modules locally
    import bz2
    import simplejson as json
    import csv
    import os
    import pyrallel
    import time
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.cli_argparse import KGTKArgumentParser
    from kgtk.exceptions import KGTKException
    from kgtk.utils.cats import platform_cat

    class MyMapper(pyrallel.Mapper):

        def enter(self):
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

            self.neg_prop_filter = {
                'P31': exclude_list,    # instance of
                'P279': exclude_list    # subclass
            }
            self.parse_labels=True
            self.parse_aliases=True
            self.parse_descr=True
            self.first=True
            self.cnt=0
            self.write_mode='w'

        def process(self,line,node_file,edge_file,qual_file,languages,doc_id):
            write_mode='a'
            if self.first==True:
                write_mode='w'
                self.first=False
            if self.cnt % 500000 == 0 and self.cnt>0:
                print("{} lines processed by processor {}".format(self.cnt,self._idx), flush=True)
            self.cnt+=1
            csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
            nrows=[]
            erows=[]
            qrows=[]
            clean_line = line.strip()
            if clean_line.endswith(b","):
                clean_line = clean_line[:-1]
            if len(clean_line) > 1:
                obj = json.loads(clean_line)
                entry_type = obj["type"]
                if entry_type == "item" or entry_type == "property":
                    keep = True
                if node_file and keep:
                    row = []
                    qnode = obj["id"]
                    row.append(qnode)

                    if self.parse_labels:
                        labels = obj["labels"]
                        label_list=[]
                        if labels:
                            for lang in languages:
                                lang_label = labels.get(lang, None)
                                if lang_label:
                                    # lang_label['value']=lang_label['value'].replace('|','\\|')
                                    # label_list.append('\'' + lang_label['value'].replace("'","\\'") + '\'' + "@" + lang)
                                    label_list.append(KgtkFormat.stringify(lang_label['value'], language=lang))
                        if len(label_list)>0:
                            row.append("|".join(label_list))
                        else:
                            row.append("")
                    row.append(entry_type)

                    if self.parse_descr:
                        descriptions = obj["descriptions"]
                        descr_list=[]
                        if descriptions:
                            for lang in languages:
                                lang_descr = descriptions.get(lang, None)
                                if lang_descr:
                                    # lang_descr['value']=lang_descr['value'].replace('|','\\|')
                                    # descr_list.append('\'' + lang_descr['value'].replace("'","\\'") + '\'' + "@" + lang)
                                    descr_list.append(KgtkFormat.stringify(lang_descr['value'], language=lang))
                        if len(descr_list)>0:
                            row.append("|".join(descr_list))
                        else:
                            row.append("")

                    if self.parse_aliases:
                        aliases = obj["aliases"]
                        alias_list = []
                        if aliases:
                            for lang in languages:
                                lang_aliases = aliases.get(lang, None)
                                if lang_aliases:
                                    for item in lang_aliases:
                                        # item['value']=item['value'].replace('|','\\|')
                                        # alias_list.append('\'' + item['value'].replace("'","\\'") + '\'' + "@" + lang)
                                        alias_list.append(KgtkFormat.stringify(item['value'], language=lang))
                        if len(alias_list)>0:
                            row.append("|".join(alias_list))
                        else:
                            row.append("")

                    #row.append(doc_id)
                    if node_file:
                        nrows.append(row)

                if edge_file or qual_file:
                    claims = obj["claims"]
                    for prop, value_set in self.neg_prop_filter.items():
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
                        sitelinks=obj.get('sitelinks',None)
                        qnode = obj["id"]
                        for prop, claim_property in claims.items():
                            seq_no = 1
                            for cp in claim_property:
                                if (deprecated or cp['rank'] != 'deprecated') and cp['mainsnak']['snaktype'] == 'value':
                                    rank=cp['rank']
                                    val = cp['mainsnak']['datavalue'].get(
                                        'value')
                                    typ = cp['mainsnak']['datatype']
                                    sid = qnode + '-' + \
                                        prop + '-' + str(seq_no)                             
                                    value = ''
                                    mag = ''
                                    unit = ''
                                    date=''
                                    item=''
                                    lower = ''
                                    upper = ''
                                    precision = ''
                                    calendar = ''
                                    lat = ''
                                    long = ''
                                    enttype = ''
                                    if typ.startswith('wikibase'):
                                        enttype = val.get('entity-type')
                                        value = val.get('id', '')
                                        item=value
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
                                            if unit not in ["undefined"]:
                                                value += unit
                                    elif typ == 'globe-coordinate':
                                        lat = str(val['latitude'])
                                        long = str(val['longitude'])
                                        precision = val.get('precision', '')
                                        value = '@' + lat + '/' + long
                                    elif typ == 'time':
                                        if val['time'][0]=='-':
                                            pre="^-"
                                        else:
                                            pre="^"
                                        date = pre + val['time'][1:]
                                        precision = str(val['precision'])
                                        calendar = val.get(
                                            'calendarmodel', '').split('/')[-1]
                                        value = pre + \
                                            val['time'][1:] + '/' + str(val['precision'])
                                    elif typ == 'monolingualtext':
                                        # value = '\'' + \
                                        # val['text'].replace("'","\\'").replace("|", "\\|") + '\'' + '@' + val['language']
                                        value = KgtkFormat.stringify(val['text'], language=val['language'])
                                    else:
                                        # value = '\"' + val.replace('"','\\"').replace("|", "\\|") + '\"'
                                        value = KgtkFormat.stringify(val)

                                    if edge_file:
                                        if explode_values:
                                            erows.append([sid,
                                                          qnode,
                                                          prop,
                                                          value,
                                                          rank,
                                                          mag,
                                                          unit,
                                                          date,
                                                          item,
                                                          lower,
                                                          upper,
                                                          lat,
                                                          long,
                                                          precision,
                                                          calendar,
                                                          enttype,
                                            ])
                                        else:
                                            erows.append([sid,
                                                          qnode,
                                                          prop,
                                                          value,
                                                          rank,
                                            ])

                                    seq_no += 1
                                    if qual_file:
                                        if cp.get('qualifiers', None):
                                            quals = cp['qualifiers']
                                            for qual_prop, qual_claim_property in quals.items():
                                                qual_seq_no = 1
                                                for qcp in qual_claim_property:
                                                    if qcp['snaktype'] == 'value':
                                                        value = ''
                                                        mag = ''
                                                        unit = ''
                                                        date= ''
                                                        item=''
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
                                                            item=value
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
                                                            if val['time'][0]=='-':
                                                                pre="^-"
                                                            else:
                                                                pre="^"
                                                            date = pre + \
                                                                val['time'][1:]
                                                            precision = str(
                                                                val['precision'])
                                                            calendar = val.get(
                                                                'calendarmodel', '').split('/')[-1]
                                                            value = pre + \
                                                                val['time'][1:] + '/' + str(val['precision'])
                                                        elif typ == 'monolingualtext':
                                                            # value = '\'' + \
                                                            #     val['text'].replace("'","\\'") + '\'' + '@' + val['language']
                                                            value = KgtkFormat.stringify(val['text'], language=val['language'])
                                                        else:
                                                            # value = '\"' + val.replace('"','\\"') + '\"'
                                                            value = KgtkFormat.stringify(val)
                                                        if explode_values:
                                                            qrows.append([
                                                                tempid,
                                                                sid,
                                                                qual_prop,
                                                                value,
                                                                mag,
                                                                unit,
                                                                date,
                                                                item,
                                                                lower,
                                                                upper,
                                                                lat,
                                                                long,
                                                                precision,
                                                                calendar,
                                                                enttype,
                                                            ])
                                                        else:
                                                            qrows.append([
                                                                tempid,
                                                                sid,
                                                                qual_prop,
                                                                value,
                                                            ])
            
                        if sitelinks:
                            wikipedia_seq_no = 1
                            for link in sitelinks:
                                if link.endswith('wiki') and link!='commonswiki':
                                    sid=qnode + '-wikipedia_sitelink-'+str(wikipedia_seq_no)
                                    wikipedia_seq_no+=1
                                    sitetitle='_'.join(sitelinks[link]['title'].split())
                                    sitelang=link.split('wiki')[0].replace('_','-')
                                    sitelink='http://'+sitelang+'.wikipedia.org/wiki/'+sitetitle
                                    if explode_values:
                                        if edge_file:
                                            erows.append([sid, qnode, 'wikipedia_sitelink', sitelink,'','','','','','','',
                                                          '','','','',''])
                                        if qual_file:
                                            tempid=sid+'-language-1'
                                            qrows.append([tempid,sid,'language',sitelang,'','','','','','','','','','',''])
                                    else:
                                        if edge_file:
                                            erows.append([sid, qnode, 'wikipedia_sitelink', sitelink,''])
                                    if qual_file:
                                        tempid=sid+'-language-1'
                                        qrows.append([tempid,sid,'language',sitelang])

            if node_file:
                with open(node_file+'_{}'.format(self._idx), write_mode, newline='') as myfile:
                    for row in nrows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='',
                            lineterminator=csv_line_terminator)
                        wr.writerow(row)
            if edge_file:
                with open(edge_file+'_{}'.format(self._idx), write_mode, newline='') as myfile:
                    for row in erows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='',
                            lineterminator=csv_line_terminator)
                        wr.writerow(row)
            if qual_file:
                with open(qual_file+'_{}'.format(self._idx), write_mode, newline='') as myfile:
                    for row in qrows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='',
                            lineterminator=csv_line_terminator)
                        wr.writerow(row)

    
    try:
        inp_path = KGTKArgumentParser.get_input_file(input_file)
        
        csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
        
        start=time.time()

        if not skip_processing:
            languages=lang.split(',')
            if node_file:
                header = ['id','label','type','description','alias']
                with open(node_file+'_header', 'w', newline='') as myfile:
                    wr = csv.writer(
                        myfile,
                        quoting=csv.QUOTE_NONE,
                        delimiter="\t",
                        escapechar="\n",
                        quotechar='',
                        lineterminator=csv_line_terminator)
                    wr.writerow(header)
            if explode_values:
                header = ['id','node1','label','node2','rank','node2;magnitude','node2;unit','node2;date','node2;item','node2;lower','node2;upper',
                          'node2;latitude','node2;longitude','node2;precision','node2;calendar','node2;entity-type']
            else:
                header = ['id','node1','label','node2', 'rank']

            if edge_file:
                with open(edge_file+'_header', 'w', newline='') as myfile:
                    wr = csv.writer(
                        myfile,
                        quoting=csv.QUOTE_NONE,
                        delimiter="\t",
                        escapechar="\n",
                        quotechar='',
                        lineterminator=csv_line_terminator)
                    wr.writerow(header)
            if qual_file:
                header.remove('rank')
                with open(qual_file+'_header', 'w', newline='') as myfile:
                    wr = csv.writer(
                        myfile,
                        quoting=csv.QUOTE_NONE,
                        delimiter="\t",
                        escapechar="\n",
                        quotechar='',
                        lineterminator=csv_line_terminator)
                    wr.writerow(header)
            pp = pyrallel.ParallelProcessor(procs, MyMapper,enable_process_id=True)
            pp.start()
            if str(inp_path).endswith(".bz2"):
                with bz2.open(inp_path, mode='rb') as file:
                    print('Decompressing and processing wikidata file %s' % str(inp_path), flush=True)
                    for cnt, line in enumerate(file):
                        if limit and cnt >= limit:
                            break
                        pp.add_task(line,node_file,edge_file,qual_file,languages,source)
            else:                             
                with open(inp_path, mode='rb') as file:
                    print('Processing wikidata file %s' % str(inp_path), flush=True)
                    for cnt, line in enumerate(file):
                        if limit and cnt >= limit:
                            break
                        pp.add_task(line,node_file,edge_file,qual_file,languages,source)

            print('Done processing {}'.format(str(inp_path)), flush=True)
            pp.task_done()
            print('Tasks done.', flush=True)
            pp.join()
            print('Join complete.', flush=True)

        if not skip_merging:
            # We've finished processing the input data, possibly using multiple
            # server processes.  We need to assemble the final output file(s) with
            # the header first, then the fragments produced by parallel
            # processing.
            #
            # If we assume that we are on Linux or MacOS, then os.sendfile(...)
            # should provide the simplest, highest-performing solution.
            if node_file:
                print('Combining the node file fragments', flush=True)
                node_file_fragments=[node_file+'_header']
                for n in range(procs):
                    node_file_fragments.append(node_file+'_'+str(n))
                platform_cat(node_file_fragments, node_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

            if edge_file:
                print('Combining the edge file fragments', flush=True)
                edge_file_fragments=[edge_file+'_header']
                for n in range(procs):
                    edge_file_fragments.append(edge_file+'_'+str(n))
                platform_cat(edge_file_fragments, edge_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

            if qual_file:
                print('Combining the qualifier file fragments', flush=True)
                qual_file_fragments=[qual_file+'_header']
                for n in range(procs):
                    qual_file_fragments.append(qual_file+'_'+str(n))
                platform_cat(qual_file_fragments, qual_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

        print('import complete', flush=True)
        end=time.time()
        print('time taken : {}s'.format(end-start), flush=True)
    except:
        raise KGTKException
