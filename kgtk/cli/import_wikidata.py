"""
Import an wikidata file into KGTK file
"""

def parser():
    return {
        'help': 'Import an wikidata file into KGTK file'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument("-i",'--inp', action="store", type=str, dest="inp_path",help='input path file')
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
    
    
def run(inp_path,procs,node_file,edge_file,qual_file,limit,lang,source,deprecated):
    # import modules locally
    import bz2
    import simplejson as json
    import csv
    import pyrallel
    import time
    import sh
    from kgtk.cli_argparse import KGTKArgumentParser
    from kgtk.exceptions import KGTKException

    

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
                print("{} lines processed by processor {}".format(self.cnt,self._idx))
            self.cnt+=1
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
                                    lang_label['value']=lang_label['value'].replace('|','\\|')
                                    label_list.append(
                                        '\'' + lang_label['value'].replace("'","\\'") + '\'' + "@" + lang)
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
                                    lang_descr['value']=lang_descr['value'].replace('|','\\|')
                                    descr_list.append(
                                        '\'' + lang_descr['value'].replace("'","\\'") + '\'' + "@" + lang)
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
                                        item['value']=item['value'].replace('|','\\|')
                                        alias_list.append(
                                            '\'' + item['value'].replace("'","\\'") + '\'' + "@" + lang)
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
                                        value = '\'' + \
                                            val['text'].replace("'","\\'") + '\'' + '@' + val['language']
                                    else:
                                        value = '\"' + val.replace('"','\\"') + '\"'
                                    if edge_file:
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
                                                     enttype])
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
                                                            value = '\'' + \
                                                                val['text'].replace("'","\\'") + '\'' + '@' + val['language']
                                                        else:
                                                            value = '\"' + val.replace('"','\\"') + '\"'
                                                        qrows.append(
                                                            [
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
                                                                enttype])
            
                        if sitelinks:
                            wikipedia_seq_no = 1
                            for link in sitelinks:
                                if link.endswith('wiki') and link!='commonswiki':
                                    sid=qnode + '-wikipedia_sitelink-'+str(wikipedia_seq_no)
                                    wikipedia_seq_no+=1
                                    sitetitle='_'.join(sitelinks[link]['title'].split())
                                    sitelang=link.split('wiki')[0].replace('_','-')
                                    sitelink='http://'+sitelang+'.wikipedia.org/wiki/'+sitetitle
                                    if edge_file:
                                        erows.append([sid, qnode, 'wikipedia_sitelink', sitelink,'','','','','','','',
                                                      '','','','',''])
                                    if qual_file:
                                        tempid=sid+'-language-1'
                                        qrows.append([tempid,sid,'language',sitelang,'','','','','','','','','','',''])

            if node_file:
                with open(node_file+'_{}'.format(self._idx), write_mode, newline='') as myfile:
                    for row in nrows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='')
                        wr.writerow(row)
            if edge_file:
                with open(edge_file+'_{}'.format(self._idx), write_mode, newline='') as myfile:
                    for row in erows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='')
                        wr.writerow(row)
            if qual_file:
                with open(qual_file+'_{}'.format(self._idx), write_mode, newline='') as myfile:
                    for row in qrows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='')
                        wr.writerow(row)
    

    
    try:
        start=time.time()
        languages=lang.split(',')
        if node_file:
            header = ['id','label','type','description','alias']
            with open(node_file+'_header', 'w', newline='') as myfile:
                wr = csv.writer(
                    myfile,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='')
                wr.writerow(header)
        header = ['id','node1','label','node2','rank','node2;magnitude','node2;unit','node2;date','node2;item','node2;lower','node2;upper',
              'node2;latitude','node2;longitude','node2;precision','node2;calendar','node2;entity-type']
        if edge_file:
            with open(edge_file+'_header', 'w', newline='') as myfile:
                wr = csv.writer(
                    myfile,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='')
                wr.writerow(header)
        if qual_file:
            header.remove('rank')
            with open(qual_file+'_header', 'w', newline='') as myfile:
                wr = csv.writer(
                    myfile,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='')
                wr.writerow(header)
        pp = pyrallel.ParallelProcessor(procs, MyMapper,enable_process_id=True)
        pp.start()
        with bz2.open(inp_path, mode='rb') as file:
            print('processing wikidata file now...')
            for cnt, line in enumerate(file):
                if limit and cnt >= limit:
                    break
                pp.add_task(line,node_file,edge_file,qual_file,languages,source)
        pp.task_done()
        pp.join()
        if node_file:
            cat_command=[node_file+'_header']
            rm_command=[node_file+'_header']
            for n in range(procs):
                cat_command.append(node_file+'_'+str(n))
                rm_command.append(node_file+'_'+str(n))
            if limit and limit==1:
                sh.cat(node_file+'_header',node_file+'_0',_out=node_file)
                sh.rm(node_file+'_header',node_file+'_0') 
            else:
                sh.cat(*cat_command,_out=node_file)
                sh.rm(*rm_command)
        if edge_file:
            cat_command=[edge_file+'_header']
            rm_command=[edge_file+'_header']
            for n in range(procs):
                cat_command.append(edge_file+'_'+str(n))
                rm_command.append(edge_file+'_'+str(n))
            if limit and limit==1:
                sh.cat(edge_file+'_header',edge_file+'_0',_out=edge_file)
                sh.rm(edge_file+'_header',edge_file+'_0') 
            else:
                sh.cat(*cat_command,_out=edge_file)
                sh.rm(*rm_command)
        if qual_file:
            cat_command=[qual_file+'_header']
            rm_command=[qual_file+'_header']
            for n in range(procs):
                cat_command.append(qual_file+'_'+str(n))
                rm_command.append(qual_file+'_'+str(n))
            if limit and limit==1:
                sh.cat(qual_file+'_header',qual_file+'_0',_out=qual_file)
                sh.rm(qual_file+'_header',qual_file+'_0') 
            else:
                sh.cat(*cat_command,_out=qual_file)
                sh.rm(*rm_command)
        print('import complete')
        end=time.time()
        print('time taken : {}s'.format(end-start))
    except:
        raise KGTKException
