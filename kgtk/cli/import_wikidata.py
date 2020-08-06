"""
Import an wikidata file into KGTK file

TODO: references

TODO: qualifiers-order

TODO: incorporate calendar into the KGTK data model.

TODO: Incorporate geographic precision into the KGTK data model.

TODO: Incorporate URLs into the KGTK data model.

TODO: Optionally select all languages for aliases, descriptions, etc.

TODO: Node type needs to be optionall in the edge file.

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

    parser.add_argument(
        "--interleave",
        nargs='?',
        type=optional_bool,
        dest="interleave",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, output the edges and qualifiers in a single file (the edge file). (default=%(default)s).",
    )

    parser.add_argument(
       "--alias-edges",
        nargs='?',
        type=optional_bool,
        dest="alias_edges",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create edge records for aliases. (default=%(default)s).",
    )

    
    parser.add_argument(
       "--description-edges",
        nargs='?',
        type=optional_bool,
        dest="descr_edges",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create edge records for descriptions. (default=%(default)s).",
    )

    
    parser.add_argument(
        "--label-edges",
        nargs='?',
        type=optional_bool,
        dest="label_edges",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create edge records for labels. (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-aliases",
        nargs='?',
        type=optional_bool,
        dest="parse_aliases",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse aliases. (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-descriptions",
        nargs='?',
        type=optional_bool,
        dest="parse_descr",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse descriptions. (default=%(default)s).",
    )
    
    parser.add_argument(
        "--parse-labels",
        nargs='?',
        type=optional_bool,
        dest="parse_labels",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse labels. (default=%(default)s).",
    )

    parser.add_argument(
        "--parse-claims",
        nargs='?',
        type=optional_bool,
        dest="parse_claims",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, parse claims. (default=%(default)s).",
    )

    parser.add_argument(
        "--fail-if-missing",
        nargs='?',
        type=optional_bool,
        dest="fail_if_missing",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, fail if expected data is missing. (default=%(default)s).",
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
        skip_merging,
        interleave,
        alias_edges,
        descr_edges,
        label_edges,
        parse_aliases,
        parse_descr,
        parse_labels,
        parse_claims,
        fail_if_missing):

    # import modules locally
    import bz2
    import simplejson as json
    import csv
    import os
    import pyrallel
    import sys
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
            self.first=True
            self.cnt=0
            self.write_mode='w'

        def erows_append(self, erows, edge_id, node1, label, node2,
                         rank="",
                         magnitude="",
                         unit="",
                         date="",
                         item="",
                         lower="",
                         upper="",
                         latitude="",
                         longitude="",
                         wikidatatype="",
                         claim_id="",
                         claim_type="",
                         val_type="",
                         entity_type="",
                         datahash="",
                         precision="",
                         calendar="",
        ):
            if len(claim_type) > 0 and claim_type != "statement":
                raise ValueError("Unexpected claim type %s" % claim_type)

            if edge_file:
                if explode_values:
                    erows.append([edge_id,
                                  node1,
                                  label,
                                  node2,
                                  rank,
                                  magnitude,
                                  unit,
                                  date,
                                  item,
                                  lower,
                                  upper,
                                  latitude,
                                  longitude,
                                  precision,
                                  calendar,
                                  entity_type,
                                  wikidatatype,
                    ])
                else:
                    erows.append([edge_id,
                                  node1,
                                  label,
                                  node2,
                                  rank,
                                  wikidatatype,
                                  claim_id,
                                  # claim_type,
                                  val_type,
                                  entity_type,
                                  datahash,
                                  precision,
                                  calendar,
                    ])

        def qrows_append(self, qrows, edge_id, node1, label, node2,
                         magnitude="",
                         unit="",
                         date="",
                         item="",
                         lower="",
                         upper="",
                         latitude="",
                         longitude="",
                         wikidatatype="",
                         val_type="",
                         entity_type="",
                         datahash="",
                         precision="",
                         calendar="",
        ):

            if qual_file:
                if explode_values:
                    qrows.append([edge_id,
                                  node1,
                                  label,
                                  node2,
                                  magnitude,
                                  unit,
                                  date,
                                  item,
                                  lower,
                                  upper,
                                  latitude,
                                  longitude,
                                  precision,
                                  calendar,
                                  entity_type,
                                  wikidatatype,
                    ])
                else:
                    qrows.append([edge_id,
                                  node1,
                                  label,
                                  node2,
                                  wikidatatype,
                                  val_type,
                                  entity_type,
                                  datahash,
                                  precision,
                                  calendar,
                    ])
                    
                
            if interleave:
                self.erows_append(erows,
                                  edge_id=edge_id,
                                  node1=node1,
                                  label=label,
                                  node2=node2,
                                  magnitude=magnitude,
                                  unit=unit,
                                  date=date,
                                  item=item,
                                  lower=lower,
                                  upper=upper,
                                  latitude=latitude,
                                  longitude=longitude,
                                  wikidatatype=wikidatatype,
                                  entity_type=entity_type,
                                  datahash=datahash,
                                  precision=precision,
                                  calendar=calendar)
            
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
                if (node_file or label_edges or alias_edges or descr_edges) and keep:
                    row = []
                    qnode = obj["id"]
                    row.append(qnode)

                    if parse_labels:
                        labels = obj.get("labels")
                        if fail_if_missing and labels is None:
                            raise KGTKException("Qnode %s is missing its labels" % qnode)
                        label_list=[]
                        if labels:
                            for lang in languages:
                                lang_label = labels.get(lang, None)
                                if lang_label:
                                    # lang_label['value']=lang_label['value'].replace('|','\\|')
                                    # label_list.append('\'' + lang_label['value'].replace("'","\\'") + '\'' + "@" + lang)
                                    value = KgtkFormat.stringify(lang_label['value'], language=lang)
                                    label_list.append(value)

                                    if label_edges and edge_file:
                                        sid = qnode + '-' + "label" + '-' + lang
                                        self.erows_append(erows,
                                                          edge_id=sid,
                                                          node1=qnode,
                                                          label="label",
                                                          node2=value)


                        if len(label_list)>0:
                            row.append("|".join(label_list))
                        else:
                            row.append("")
                    row.append(entry_type)

                    if parse_descr:
                        descriptions = obj.get("descriptions")
                        if fail_if_missing and descriptions is None:
                            raise KGTKException("Qnode %s is missing its descriptions" % qnode)
                        descr_list=[]
                        if descriptions:
                            for lang in languages:
                                lang_descr = descriptions.get(lang, None)
                                if lang_descr:
                                    # lang_descr['value']=lang_descr['value'].replace('|','\\|')
                                    # descr_list.append('\'' + lang_descr['value'].replace("'","\\'") + '\'' + "@" + lang)
                                    value = KgtkFormat.stringify(lang_descr['value'], language=lang)
                                    descr_list.append(value)
                                    if descr_edges and edge_file:
                                        sid = qnode + '-' + "description" + '-' + lang
                                        self.erows_append(erows,
                                                          edge_id=sid,
                                                          node1=qnode,
                                                          label="description",
                                                          node2=value)

                        if len(descr_list)>0:
                            row.append("|".join(descr_list))
                        else:
                            row.append("")

                    if parse_aliases:
                        aliases = obj.get("aliases")
                        if fail_if_missing and aliases is None:
                            raise KGTKException("Qnode %s is missing its aliases" % qnode)
                        alias_list = []
                        if aliases:
                            for lang in languages:
                                seq_no = 1
                                lang_aliases = aliases.get(lang, None)
                                if lang_aliases:
                                    for item in lang_aliases:
                                        # item['value']=item['value'].replace('|','\\|')
                                        # alias_list.append('\'' + item['value'].replace("'","\\'") + '\'' + "@" + lang)
                                        value = KgtkFormat.stringify(item['value'], language=lang)
                                        alias_list.append(value)
                                        if alias_edges and edge_file:
                                            sid = qnode + '-' + "alias" + "-" + lang + '-' + str(seq_no)
                                            seq_no += 1
                                            self.erows_append(erows,
                                                              edge_id=sid,
                                                              node1=qnode,
                                                              label="alias",
                                                              node2=value)


                        if len(alias_list)>0:
                            row.append("|".join(alias_list))
                        else:
                            row.append("")

                    #row.append(doc_id)
                    if node_file:
                        nrows.append(row)

                if (edge_file or qual_file) and parse_claims and "claims" not in obj:
                    if fail_if_missing:
                            raise KGTKException("Qnode %s is missing its claims" % qnode)
                    
                if (edge_file or qual_file) and parse_claims and "claims" in obj:
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
                                if (deprecated or cp['rank'] != 'deprecated'):
                                    snaktype = cp['mainsnak']['snaktype']
                                    rank=cp['rank']
                                    claim_id = cp['id']
                                    claim_type = cp['type']
                                    if claim_type != "statement":
                                        print("Unknown claim type %s" % claim_type, file=sys.stderr, flush=True)

                                    if snaktype == 'value':
                                        datavalue = cp['mainsnak']['datavalue']
                                        val = datavalue.get('value')
                                        val_type = datavalue.get("type", "")
                                    elif snaktype == 'somevalue':
                                        val = None
                                        val_type = ""
                                    else:
                                        raise ValueError("Unknown snaktype %s" % snaktype)

                                    typ = cp['mainsnak']['datatype']
                                    # if typ != val_type:
                                    #     print("typ %s != val_type %s" % (typ, val_type), file=sys.stderr, flush=True)

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

                                    if val is None:
                                        value = "somevalue"
                                    elif typ.startswith('wikibase'):
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
                                        # TODO: what about "globe"?
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
                                        self.erows_append(erows,
                                                          edge_id=sid,
                                                          node1=qnode,
                                                          label=prop,
                                                          node2=value,
                                                          rank=rank,
                                                          magnitude=mag,
                                                          unit=unit,
                                                          date=date,
                                                          item=item,
                                                          lower=lower,
                                                          upper=upper,
                                                          latitude=lat,
                                                          longitude=long,
                                                          wikidatatype=typ,
                                                          claim_id=claim_id,
                                                          claim_type=claim_type,
                                                          val_type=val_type,
                                                          entity_type=enttype,
                                                          precision=precision,
                                                          calendar=calendar)

                                    seq_no += 1
                                    if qual_file or interleave:
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
                                                        datahash = qcp['hash']
                                                        datavalue = qcp['datavalue']
                                                        val = datavalue.get('value')
                                                        val_type = datavalue.get("type", "")
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
                                                        self.qrows_append(qrows,
                                                                          edge_id=tempid,
                                                                          node1=sid,
                                                                          label=qual_prop,
                                                                          node2=value,
                                                                          magnitude=mag,
                                                                          unit=unit,
                                                                          date=date,
                                                                          item=item,
                                                                          lower=lower,
                                                                          upper=upper,
                                                                          latitude=lat,
                                                                          longitude=long,
                                                                          wikidatatype=typ,
                                                                          entity_type=enttype,
                                                                          datahash=datahash,
                                                                          precision=precision,
                                                                          calendar=calendar)
                                                        
                        if sitelinks:
                            wikipedia_seq_no = 1
                            for link in sitelinks:
                                # TODO: If the title might contain vertical bar, more work is needed
                                # to make the sitetitle safe for KGTK.
                                if link.endswith('wiki') and link not in ('commonswiki', 'simplewiki'):
                                    linklabel = 'wikipedia_sitelink'
                                    sid=qnode + '-' + linklabel + '-'+str(wikipedia_seq_no)
                                    wikipedia_seq_no+=1
                                    sitetitle='_'.join(sitelinks[link]['title'].split())
                                    sitelang=link.split('wiki')[0].replace('_','-')
                                    sitelink='http://'+sitelang+'.wikipedia.org/wiki/'+sitetitle
                                else:
                                    linklabel = 'addl_wikipedia_sitelink'
                                    sid=qnode + '-' + linklabel + '-'+str(wikipedia_seq_no)
                                    wikipedia_seq_no+=1
                                    sitetitle='_'.join(sitelinks[link]['title'].split())
                                    if "wiki" in link:
                                        sitelang=link.split("wiki")[0]
                                        if sitelang in ("commons", "simple"):
                                            sitelang = "en"
                                    else:
                                        sitelang=""
                                    sitehost=link+'.org' # TODO: Needs more work here
                                    sitelink = 'http://'+sitehost+'/wiki/'+sitetitle

                                if sitelink is not None:
                                    if edge_file:
                                        self.erows_append(erows,
                                                          edge_id=sid,
                                                          node1=qnode,
                                                          label=linklabel,
                                                          node2=sitelink)
                                    if qual_file or interleave:
                                        if len(sitelang) > 0:
                                            tempid=sid+'-language-1'
                                            self.qrows_append(qrows,
                                                              edge_id=tempid,
                                                              node1=sid,
                                                              label='language',
                                                              node2=sitelang)

                                        tempid=sid+'-site-1'
                                        self.qrows_append(qrows,
                                                          edge_id=tempid,
                                                          node1=sid,
                                                          label='site',
                                                          node2=link)

                                        tempid=sid+'-title-1'
                                        self.qrows_append(qrows,
                                                          edge_id=tempid,
                                                          node1=sid,
                                                          label='title',
                                                          node2=KgtkFormat.stringify(sitelinks[link]['title']))

                                        badge_num: int = 0
                                        for badge in sitelinks[link]['badges']:
                                            tempid=sid+'-badge-'+str(badge_num + 1)
                                            self.qrows_append(qrows,
                                                              edge_id=tempid,
                                                              node1=sid,
                                                              label='badge',
                                                              node2=sitelinks[link]['badges'][badge_num])
                                            badge_num += 1

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
        UPDATE_VERSION: str = "2020-07-23T02:02:15.389869+00:00#TN1Bg8DKAzP7+I3bjT+HJHkauAxEWg73CNCjkdY1eLw716rcAe/Lv34DJwkeSoI115UxEQnBwAlqqv6cCsx3Nw=="
        print("kgtk import-wikidata version: %s" % UPDATE_VERSION, flush=True)

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
                          'node2;latitude','node2;longitude','node2;precision','node2;calendar','node2;entity-type','node2;wikidatatype']
            else:
                header = ['id','node1','label','node2',
                          'rank', 'node2;wikidatatype',
                          'claim_id', 'val_type', 'entity_type', 'datahash', 'precision', 'calendar']

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
                if "rank" in header:
                    header.remove('rank')
                if "claim_type" in header:
                    header.remove('claim_type')
                if "claim_id" in header:
                    header.remove('claim_id')
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
