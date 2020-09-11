"""
Import an wikidata file into KGTK file

TODO: references

TODO: qualifiers-order

TODO: incorporate calendar into the KGTK data model.

TODO: Incorporate geographic precision into the KGTK data model.

TODO: Incorporate URLs into the KGTK data model.

TODO: Node type needs to be optional in the edge file.

"""

import typing
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
        help='number of processes to run in parallel, default %(default)d')

    parser.add_argument(
        '--max-size-per-mapper-queue',
        action="store",
        type=int,
        dest="max_size_per_mapper_queue",
        default=4,
        help='max depth of server queues, default %(default)d')

    parser.add_argument(
        '--mapper-batch-size',
        action="store",
        type=int,
        dest="mapper_batch_size",
        default=5,
        help='How many statements to queue in a batch to a worker. (default=%(default)d)')

    parser.add_argument(
        "--single-mapper-queue",
        nargs='?',
        type=optional_bool,
        dest="single_mapper_queue",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, use a single queue for worker tasks.  If false, each worker has its own task queue. (default=%(default)s).",
    )

    parser.add_argument(
        "--collect-results",
        nargs='?',
        type=optional_bool,
        dest="collect_results",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, collect the results before writing to disk.  If false, write results to disk, then concatenate. (default=%(default)s).",
    )

    parser.add_argument(
        "--collect-seperately",
        nargs='?',
        type=optional_bool,
        dest="collect_seperately",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, collect the node, edge, and qualifier results using seperate processes.  If false, collect the results with a single process. (default=%(default)s).",
    )

    parser.add_argument(
        '--collector-batch-size',
        action="store",
        type=int,
        dest="collector_batch_size",
        default=5,
        help='How many statements to queue in a batch to the collector. (default=%(default)d)')

    parser.add_argument(
        "--use-shm",
        nargs='?',
        type=optional_bool,
        dest="use_shm",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, use ShmQueue. (default=%(default)s).")

    parser.add_argument(
        '--collector-queue-per-proc-size',
        action="store",
        type=int,
        dest="collector_queue_per_proc_size",
        default=2,
        help='collector queue depth per proc, default %(default)d')

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
        "--entry-type-edges",
        nargs='?',
        type=optional_bool,
        dest="entry_type_edges",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create edge records for the entry type field. (default=%(default)s).",
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
       "--datatype-edges",
        nargs='?',
        type=optional_bool,
        dest="datatype_edges",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, create edge records for property datatypes. (default=%(default)s).",
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

    parser.add_argument(
        "--all-languages",
        nargs='?',
        type=optional_bool,
        dest="all_languages",
        const=True,
        default=False,
        metavar="True/False",
        help="If true, override --lang and import aliases, dscriptions, and labels in all languages. (default=%(default)s).",
    )
    
    parser.add_argument(
        "--warn-if-missing",
        nargs='?',
        type=optional_bool,
        dest="warn_if_missing",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, print a warning message if expected data is missing. (default=%(default)s).",
    )

    parser.add_argument(
        '--progress-interval',
        action="store",
        type=int,
        dest="progress_interval",
        default=500000,
        help='How often to report progress. (default=%(default)d)')
    
    parser.add_argument(
        "--use-kgtkwriter",
        nargs='?',
        type=optional_bool,
        dest="use_kgtkwriter",
        const=True,
        default=True,
        metavar="True/False",
        help="If true, use KgtkWriter instead of csv.writer. (default=%(default)s).")

def run(input_file: KGTKFiles,
        procs: int,
        max_size_per_mapper_queue: int,
        node_file: typing.Optional[str],
        edge_file: typing.Optional[str],
        qual_file: typing.Optional[str],
        limit: int,
        lang: str,
        source: str,
        deprecated: bool,
        explode_values: bool,
        use_python_cat: bool,
        keep_temp_files: bool,
        skip_processing: bool,
        skip_merging: bool,
        interleave: bool,
        entry_type_edges: bool,
        alias_edges: bool,
        datatype_edges: bool,
        descr_edges: bool,
        label_edges: bool,
        parse_aliases: bool,
        parse_descr: bool,
        parse_labels: bool,
        parse_claims: bool,
        fail_if_missing: bool,
        all_languages: bool,
        warn_if_missing: bool,
        collect_results: bool,
        collect_seperately: bool,
        collector_queue_per_proc_size: int,
        progress_interval: int,
        use_shm: bool,
        mapper_batch_size: int,
        collector_batch_size: int,
        single_mapper_queue: bool,
        use_kgtkwriter: bool,
        ):

    # import modules locally
    import bz2
    import simplejson as json
    import csv
    import gzip
    import multiprocessing as mp
    import os
    from pathlib import Path
    import pyrallel
    import sys
    import time
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.cli_argparse import KGTKArgumentParser
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.utils.cats import platform_cat

    collector_q: typing.Optional[pyrallel.ShmQueue] = None
    node_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    edge_collector_q: typing.Optional[pyrallel.ShmQueue] = None
    qual_collector_q: typing.Optional[pyrallel.ShmQueue] = None

    class MyMapper(pyrallel.Mapper):

        def enter(self):
            print("Starting worker process {} (pid {}).".format(self._idx, os.getpid()), file=sys.stderr, flush=True)
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

            
            self.node_f = None
            if node_file and not collect_results:
                self.node_f = open(node_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.node_wr = csv.writer(
                    self.node_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                
            self.edge_f = None
            if edge_file and not collect_results:
                self.edge_f = open(edge_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.edge_wr = csv.writer(
                    self.edge_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                
            self.qual_f = None
            if qual_file and not collect_results:
                self.qual_f = open(qual_file+'_{}'.format(self._idx), self.write_mode, newline='')
                self.qual_wr = csv.writer(
                    self.qual_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)

            if collect_results and collector_batch_size > 1:
                self.collector_batch_cnt = 0
                self.collector_nrows_batch = [ ]
                self.collector_erows_batch = [ ]
                self.collector_qrows_batch = [ ]


        def exit(self, *args, **kwargs):
            print("Exiting worker process {} (pid {}).".format(self._idx, os.getpid()), file=sys.stderr, flush=True)
            if collect_results:
                if collector_batch_size > 1:
                    if len(self.collector_nrows_batch) > 0 or len(self.collector_erows_batch) > 0 or len(self.collector_qrows_batch) > 0:
                        if collect_seperately:
                            if len(self.collector_nrows_batch) > 0:
                                node_collector_q.put(("rows", self.collector_nrows_batch, [], [], None))
                            if len(self.collector_erows_batch) > 0:
                                edge_collector_q.put(("rows", [], self.collector_erows_batch, [], None))
                            if len(self.collector_qrows_batch) > 0:
                                qual_collector_q.put(("rows", [], [], self.collector_qrows_batch, None))
                        else:
                            collector_q.put(("rows", self.collector_nrows_batch, self.collector_erows_batch, self.collector_qrows_batch, None))
                        
            else:
                if self.node_f is not None:
                    self.node_f.close()

                if self.edge_f is not None:
                    self.edge_f.close()

                if self.qual_f is not None:
                    self.qual_f.close()

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
            
        # def process(self,line,node_file,edge_file,qual_file,languages,source):
        def process(self, line):
            if progress_interval > 0 and self.cnt % progress_interval == 0 and self.cnt>0:
                print("{} lines processed by processor {}".format(self.cnt,self._idx), file=sys.stderr, flush=True)
            self.cnt+=1
            # csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
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
                elif warn_if_missing:
                    print("Unknown object type {}.".format(entry_type), file=sys.stderr, flush=True)
                if (node_file or entry_type_edges or label_edges or alias_edges or descr_edges) and keep:
                    row = []
                    qnode = obj["id"]
                    row.append(qnode)

                    if parse_labels:
                        labels = obj.get("labels")
                        if labels is None:
                            if fail_if_missing:
                                raise KGTKException("Qnode %s is missing its labels" % qnode)
                            elif warn_if_missing:
                                print("Object id {} has no labels.".format(qnode), file=sys.stderr, flush=True)
                        label_list=[]
                        if labels:
                            if all_languages:
                                label_languages = labels.keys()
                            else:
                                label_languages = languages
                            for lang in label_languages:
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
                    if entry_type_edges and edge_file:
                        sid = qnode + '-' + "type"
                        self.erows_append(erows,
                                          edge_id=sid,
                                          node1=qnode,
                                          label="type",
                                          node2=entry_type)

                    if parse_descr:
                        descriptions = obj.get("descriptions")
                        if descriptions is None:
                            if fail_if_missing:
                                raise KGTKException("Qnode %s is missing its descriptions" % qnode)
                            elif warn_if_missing:
                                print("Object id {} has no descriptions.".format(qnode), file=sys.stderr, flush=True)
                        descr_list=[]
                        if descriptions:
                            if all_languages:
                                desc_languages = descriptions.keys()
                            else:
                                desc_languages = languages
                            for lang in desc_languages:
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
                        if aliases is None:
                            if fail_if_missing:
                                raise KGTKException("Qnode %s is missing its aliases" % qnode)
                            elif warn_if_missing:
                                print("Object id {} has no aliasees.".format(qnode), file=sys.stderr, flush=True)
                        alias_list = []
                        if aliases:
                            if all_languages:
                                alias_languages = aliases.keys()
                            else:
                                alias_languages = languages
                            for lang in alias_languages:
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

                    datatype = obj.get("datatype", "")
                    row.append(datatype)
                    if len(datatype) > 0 and datatype_edges and edge_file:
                        sid = qnode + '-' + "datatype"
                        # We expect the datatype to be a valid KGTK symbol, so
                        # there's no need to stringify it.
                        self.erows_append(erows,
                                          edge_id=sid,
                                          node1=qnode,
                                          label="datatype",
                                          node2=datatype)
                    
                    #row.append(source)
                    if node_file:
                        nrows.append(row)

                if (edge_file or qual_file) and parse_claims and "claims" not in obj:
                    if fail_if_missing:
                        raise KGTKException("Qnode %s is missing its claims" % qnode)
                    elif warn_if_missing:
                        print("Object id {} is missing its claims.".format(qnode), file=sys.stderr, flush=True)
                    
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
                                        val_type = "somevalue"
                                    elif snaktype == 'novalue':
                                        val = None
                                        val_type = "novalue"
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
                                        value = val_type
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
                                        # TODO: Don't lose the single-character unit code.  At a minimum, verify that it is the value "1".
                                        if len(val.get('unit')) > 1:
                                            unit = val.get(
                                                'unit').split('/')[-1]
                                            if unit not in ["undefined"]:
                                                # TODO: don't lose track of "undefined" units.
                                                value += unit
                                    elif typ == 'globe-coordinate':
                                        lat = str(val['latitude'])
                                        long = str(val['longitude'])
                                        precision = str(val.get('precision', ''))
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

                                                    snaktype = qcp['snaktype']
                                                    if snaktype == 'value':
                                                        datavalue = qcp['datavalue']
                                                        val = datavalue.get('value')
                                                        val_type = datavalue.get("type", "")
                                                    elif snaktype == 'somevalue':
                                                        val = None
                                                        val_type = "somevalue"
                                                    elif snaktype == 'novalue':
                                                        val = None
                                                        val_type = "novalue"
                                                    else:
                                                        raise ValueError("Unknown qualifier snaktype %s" % snaktype)

                                                    if True:
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
                                                        datahash = '"' + qcp['hash'] + '"'
                                                        typ = qcp['datatype']
                                                        tempid = sid + '-' + qual_prop + \
                                                            '-' + str(qual_seq_no)
                                                        qual_seq_no += 1

                                                        if val is None:
                                                            value = val_type

                                                        elif typ.startswith(
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
                                                            precision = str(val.get(
                                                                'precision', ''))
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

            if len(nrows) > 0 or len(erows) > 0 or len(qrows) > 0:               
                if collect_results:
                    if collector_batch_size == 1:
                        if collect_seperately:
                            if len(nrows) > 0 and node_collector_q is not None:
                                node_collector_q.put(("rows", nrows, [], [], None))
                            if len(erows) > 0 and edge_collector_q is not None:
                                edge_collector_q.put(("rows", [], erows, [], None))
                            if len(qrows) > 0 and qual_collector_q is not None:
                                qual_collector_q.put(("rows", nrows, [], [], None))
                        elif collector_q is not None:
                            collector_q.put(("rows", nrows, erows, qrows, None))
                    else:
                        self.collector_nrows_batch.extend(nrows)
                        self.collector_erows_batch.extend(erows)
                        self.collector_qrows_batch.extend(qrows)
                        self.collector_batch_cnt += 1

                        if self.collector_batch_cnt >= collector_batch_size:
                            if collect_seperately:
                                if len(self.collector_nrows_batch) > 0 and node_collector_q is not None:
                                    node_collector_q.put(("rows", self.collector_nrows_batch, [], [], None))
                                if len(self.collector_erows_batch) > 0 and edge_collector_q is not None:
                                    edge_collector_q.put(("rows", [], self.collector_erows_batch, [], None))
                                if len(self.collector_qrows_batch) > 0 and qual_collector_q is not None:
                                    qual_collector_q.put(("rows", [], [], self.collector_qrows_batch, None))
                            elif collector_q is not None:
                                collector_q.put(("rows", self.collector_nrows_batch, self.collector_erows_batch, self.collector_qrows_batch, None))

                            self.collector_nrows_batch.clear()
                            self.collector_erows_batch.clear()
                            self.collector_qrows_batch.clear()
                            self.collector_batch_cnt = 0

                else:
                    if node_file:
                        for row in nrows:
                            self.node_wr.writerow(row)

                    if edge_file:
                        for row in erows:
                            self.edge_wr.writerow(row)

                    if qual_file:
                        for row in qrows:
                            self.qual_wr.writerow(row)
    
    class MyCollector:

        def __init__(self):
            # Prepare to use the collector.
            self.node_f: typing.Optional[typing.TextIO] = None
            self.node_wr = None
            self.nrows: int = 0

            self.edge_f: typing.Optional[typing.TextIO] = None
            self.edge_wr = None
            self.erows: int = 0

            self.qual_f: typing.Optional[typing.TextIO] = None
            self.qual_wr = None
            self.qrows: int = 0

            self.cnt: int = 0

            self.started: bool = False

        def run(self,
                node_file: typing.Optional[str],
                edge_file: typing.Optional[str],
                qual_file: typing.Optional[str],
                collector_q,
                who: str):
            print("The %s collector is starting (pid %d)." % (who, os.getpid()), file=sys.stderr, flush=True)
                
            while True:
                action, nrows, erows, qrows, header = collector_q.get()
                # print("Collector action %s." % action, file=sys.stderr, flush=True)

                if action == "rows":
                    self.collect(nrows, erows, qrows, who)

                elif action == "node_header":
                    self.open_node_file(node_file, header, who)

                elif action == "edge_header":
                    self.open_edge_file(edge_file, header, who)

                elif action == "qual_header":
                    self.open_qual_file(qual_file, header, who)

                elif action == "shutdown":
                    self.shutdown(who)
                    break

        def open_node_file(self, node_file: typing.Optional[str], header: typing.List[str], who: str):
            if node_file is None or len(node_file) == 0:
                raise ValueError("Node header without a node file in the %s collector." % who)

            if use_kgtkwriter:
                print("Opening the node file in the %s collector with KgtkWriter." % who, file=sys.stderr, flush=True)
                self.node_wr = KgtkWriter.open(header, Path(node_file), who=who + " collector")
                
            else:
                print("Opening the node file in the %s collector with csv.writer." % who, file=sys.stderr, flush=True)
                csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
                self.node_f = open(node_file, "w", newline='')
                self.node_wr = csv.writer(
                    self.node_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                self.node_wr.writerow(header)

        def open_edge_file(self, edge_file: typing.Optional[str], header: typing.List[str], who: str):
            if edge_file is None or len(edge_file) == 0:
                raise ValueError("Edge header without an edge file in the %s collector." % who)

            if use_kgtkwriter:
                print("Opening the edge file in the %s collector with KgtkWriter." % who, file=sys.stderr, flush=True)
                self.edge_wr = KgtkWriter.open(header, Path(edge_file), who=who + " collector")
                
            else:
                print("Opening the edge file in the %s collector with csv.writer." % who, file=sys.stderr, flush=True)
                csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
                self.edge_f = open(edge_file, "w", newline='')
                self.edge_wr = csv.writer(
                    self.edge_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                self.edge_wr.writerow(header)

        def open_qual_file(self, qual_file: typing.Optional[str], header: typing.List[str], who: str):
            if qual_file is None or len(qual_file) == 0:
                raise ValueError("Qual header without a qual file in the %s collector." % who)

            if use_kgtkwriter:
                print("Opening the qual file in the %s collector with KgtkWriter." % who, file=sys.stderr, flush=True)
                self.qual_wr = KgtkWriter.open(header, Path(qual_file), who=who + " collector")
                
            else:
                print("Opening the qual file in the %s collector with csv.writer." % who, file=sys.stderr, flush=True)
                csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
                self.qual_f = open(qual_file, "w", newline='')
                self.qual_wr = csv.writer(
                    self.qual_f,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='',
                    lineterminator=csv_line_terminator)
                self.qual_wr.writerow(header)
            
        def shutdown(self, who: str):
            print("Exiting the %s collector (pid %d)." % (who, os.getpid()), file=sys.stderr, flush=True)

            if use_kgtkwriter:
                if self.node_wr is not None:
                    self.node_wr.close()
                if self.edge_wr is not None:
                    self.edge_wr.close()
                if self.qual_wr is not None:
                    self.qual_wr.close()

            else:
                if self.node_f is not None:
                    self.node_f.close()

                if self.edge_f is not None:
                    self.edge_f.close()

                if self.qual_f is not None:
                    self.qual_f.close()

            print("The %s collector has closed its output files." % who, file=sys.stderr, flush=True)

        def collect(self, nrows, erows, qrows, who: str):
            self.nrows += len(nrows)
            self.erows += len(erows)
            self.qrows += len(qrows)

            self.cnt += 1
            if progress_interval > 0 and self.cnt % progress_interval == 0:
                print("The {} collector called {} times: {} nrows, {} erows, {} qrows".format(who,
                                                                                              self.cnt,
                                                                                              self.nrows,
                                                                                              self.erows,
                                                                                              self.qrows), file=sys.stderr, flush=True)
            if self.node_wr is not None:
                if use_kgtkwriter:
                    for row in nrows:
                        self.node_wr.write(row)
                else:
                    self.node_wr.writerows(nrows)
            elif len(nrows) > 0:
                raise ValueError("Unexpected node rows in the %s collector." % who)

            if self.edge_wr is not None:
                if use_kgtkwriter:
                    for row in erows:
                        self.edge_wr.write(row)
                else:
                    self.edge_wr.writerows(erows)
            elif len(erows) > 0:
                raise ValueError("Unexpected edge rows in the %s collector." % who)

            if self.qual_wr is not None:
                if use_kgtkwriter:
                    for row in qrows:
                        self.qual_wr.write(row)
                else:
                    self.qual_wr.writerows(qrows)
            elif len(qrows) > 0:
                raise ValueError("Unexpected qual rows in the %s collector." % who)

    try:
        UPDATE_VERSION: str = "2020-09-10T22:20:40.879539+00:00#H/efBooi/N4ZmRwyM0xEJqu3HLU6XzsVhLtueht4KjGlvH/QjJE33MtEXrpD1NZkem6nJYhhQEcFz+wJqea4TQ=="
        print("kgtk import-wikidata version: %s" % UPDATE_VERSION, file=sys.stderr, flush=True)
        print("Starting main process (pid %d)." % os.getpid(), file=sys.stderr, flush=True)
        inp_path = KGTKArgumentParser.get_input_file(input_file)
        
        csv_line_terminator = "\n" if os.name == 'posix' else "\r\n"
        
        start=time.time()

        if not skip_processing:
            print("Processing.", file=sys.stderr, flush=True)
            languages=lang.split(',')

            input_f: typing.IO[typing.Any]
            # Open the input file first to make it easier to monitor with "pv".
            if str(inp_path).endswith(".bz2"):
                print('Decompressing (bz2) and processing wikidata file %s' % str(inp_path), file=sys.stderr, flush=True)
                input_f = bz2.open(inp_path, mode='rb')

            elif str(inp_path).endswith(".gz"):
                print('Decompressing (gzip) and processing wikidata file %s' % str(inp_path), file=sys.stderr, flush=True)
                input_f = gzip.open(inp_path, mode='rb')

            else:                             
                print('Processing wikidata file %s' % str(inp_path), file=sys.stderr, flush=True)
                input_f = open(inp_path, mode='rb')

            collector_p = None
            node_collector_p = None
            edge_collector_p = None
            qual_collector_p = None

            if collect_results:
                print("Creating the collector queue.", file=sys.stderr, flush=True)
                # collector_q = pyrallel.ShmQueue()
                collector_q_maxsize = procs*collector_queue_per_proc_size
                if collect_seperately:

                    if node_file is not None:
                        node_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector node queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)
                
                        print("Creating the node_collector.", file=sys.stderr, flush=True)
                        node_collector: MyCollector = MyCollector()
                        print("Creating the node collector process.", file=sys.stderr, flush=True)
                        node_collector_p = mp.Process(target=node_collector.run, args=(node_file, None, None, node_collector_q, "node"))
                        print("Starting the node collector process.", file=sys.stderr, flush=True)
                        node_collector_p.start()
                        print("Started the node collector process.", file=sys.stderr, flush=True)

                    if edge_file is not None:
                        edge_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector edge queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the edge_collector.", file=sys.stderr, flush=True)
                        edge_collector: MyCollector = MyCollector()
                        print("Creating the edge collector process.", file=sys.stderr, flush=True)
                        edge_collector_p = mp.Process(target=edge_collector.run, args=(None, edge_file, None, edge_collector_q, "edge"))
                        print("Starting the edge collector process.", file=sys.stderr, flush=True)
                        edge_collector_p.start()
                        print("Started the edge collector process.", file=sys.stderr, flush=True)

                    if qual_file is not None:
                        qual_collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                        print("The collector qual queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)

                        print("Creating the qual_collector.", file=sys.stderr, flush=True)
                        qual_collector: MyCollector = MyCollector()
                        print("Creating the qual collector process.", file=sys.stderr, flush=True)
                        qual_collector_p = mp.Process(target=qual_collector.run, args=(None, None, qual_file, qual_collector_q, "qual"))
                        print("Starting the qual collector process.", file=sys.stderr, flush=True)
                        qual_collector_p.start()
                        print("Started the qual collector process.", file=sys.stderr, flush=True)

                else:
                    collector_q = pyrallel.ShmQueue(maxsize=collector_q_maxsize)
                    print("The common collector queue has been created (maxsize=%d)." % collector_q_maxsize, file=sys.stderr, flush=True)
                
                    print("Creating the common collector.", file=sys.stderr, flush=True)
                    collector: MyCollector = MyCollector()
                    print("Creating the common collector process.", file=sys.stderr, flush=True)
                    collector_p = mp.Process(target=collector.run, args=(node_file, edge_file, qual_file, collector_q, "common"))
                    print("Starting the common collector process.", file=sys.stderr, flush=True)
                    collector_p.start()
                    print("Started the common collector process.", file=sys.stderr, flush=True)

            if node_file:
                header = ['id','label','type','description','alias','datatype']
                if collector_q is not None:
                    print("Sending the node header to the collector.", file=sys.stderr, flush=True)
                    collector_q.put(("node_header", None, None, None, header))
                    print("Sent the node header to the collector.", file=sys.stderr, flush=True)

                elif node_collector_q is not None:
                    print("Sending the node header to the node collector.", file=sys.stderr, flush=True)
                    node_collector_q.put(("node_header", None, None, None, header))
                    print("Sent the node header to the node collector.", file=sys.stderr, flush=True)

                else:
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
                if collector_q is not None:
                    print("Sending the edge header to the collector.", file=sys.stderr, flush=True)
                    collector_q.put(("edge_header", None, None, None, header))
                    print("Sent the edge header to the collector.", file=sys.stderr, flush=True)

                elif edge_collector_q is not None:
                    print("Sending the edge header to the edge collector.", file=sys.stderr, flush=True)
                    edge_collector_q.put(("edge_header", None, None, None, header))
                    print("Sent the edge header to the edge collector.", file=sys.stderr, flush=True)

                else:
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

                if collector_q is not None:
                    print("Sending the qual header to the collector.", file=sys.stderr, flush=True)
                    collector_q.put(("qual_header", None, None, None, header))
                    print("Sent the qual header to the collector.", file=sys.stderr, flush=True)

                elif qual_collector_q is not None:
                    print("Sending the qual header to the qual collector.", file=sys.stderr, flush=True)
                    qual_collector_q.put(("qual_header", None, None, None, header))
                    print("Sent the qual header to the qual collector.", file=sys.stderr, flush=True)

                else:
                    with open(qual_file+'_header', 'w', newline='') as myfile:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='',
                            lineterminator=csv_line_terminator)
                        wr.writerow(header)

            print('Creating parallel processor for {}'.format(str(inp_path)), file=sys.stderr, flush=True)
            pp = pyrallel.ParallelProcessor(procs, MyMapper,enable_process_id=True, max_size_per_mapper_queue=max_size_per_mapper_queue,
                                            use_shm=use_shm, enable_collector_queues=False, batch_size=mapper_batch_size,
                                            single_mapper_queue=single_mapper_queue)
            print('Start parallel processing', file=sys.stderr, flush=True)
            pp.start()
            for cnt, line in enumerate(input_f):
                if limit and cnt >= limit:
                    break
                # pp.add_task(line,node_file,edge_file,qual_file,languages,source)
                pp.add_task(line)

            print('Done processing {}'.format(str(inp_path)), file=sys.stderr, flush=True)
            input_f.close()
            
            print('Telling the workers to shut down.', file=sys.stderr, flush=True)
            pp.task_done()
            print('Waiting for the workers to shut down.', file=sys.stderr, flush=True)
            pp.join()
            print('Worker shut down is complete.', file=sys.stderr, flush=True)

            if collector_q is not None:
                print('Telling the collector to shut down.', file=sys.stderr, flush=True)
                collector_q.put(("shutdown", None, None, None, None))
            if collector_p is not None:
                print('Waiting for the collector to shut down.', file=sys.stderr, flush=True)
                collector_p.join()
                print('Collector shut down is complete.', file=sys.stderr, flush=True)
            if collector_q is not None:
                collector_q.close()

            if node_collector_q is not None:
                print('Telling the node collector to shut down.', file=sys.stderr, flush=True)
                node_collector_q.put(("shutdown", None, None, None, None))
            if node_collector_p is not None:
                print('Waiting for the node collector to shut down.', file=sys.stderr, flush=True)
                node_collector_p.join()
                print('Node collector shut down is complete.', file=sys.stderr, flush=True)
            if node_collector_q is not None:
                node_collector_q.close()

            if edge_collector_q is not None:
                print('Telling the edge collector to shut down.', file=sys.stderr, flush=True)
                edge_collector_q.put(("shutdown", None, None, None, None))
            if edge_collector_p is not None:
                print('Waiting for the edge collector to shut down.', file=sys.stderr, flush=True)
                edge_collector_p.join()
                print('Edge collector shut down is complete.', file=sys.stderr, flush=True)
            if edge_collector_q is not None:
                edge_collector_q.close()

            if qual_collector_q is not None:
                print('Telling the qual collector to shut down.', file=sys.stderr, flush=True)
                qual_collector_q.put(("shutdown", None, None, None, None))
            if qual_collector_p is not None:
                print('Waiting for the qual collector to shut down.', file=sys.stderr, flush=True)
                qual_collector_p.join()
                print('Qual collector shut down is complete.', file=sys.stderr, flush=True)
            if qual_collector_q is not None:
                qual_collector_q.close()

        if not skip_merging and not collect_results:
            # We've finished processing the input data, possibly using multiple
            # server processes.  We need to assemble the final output file(s) with
            # the header first, then the fragments produced by parallel
            # processing.
            #
            # If we assume that we are on Linux, then os.sendfile(...)
            # should provide the simplest, highest-performing solution.
            if node_file:
                print('Combining the node file fragments', file=sys.stderr, flush=True)
                node_file_fragments=[node_file+'_header']
                for n in range(procs):
                    node_file_fragments.append(node_file+'_'+str(n))
                platform_cat(node_file_fragments, node_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

            if edge_file:
                print('Combining the edge file fragments', file=sys.stderr, flush=True)
                edge_file_fragments=[edge_file+'_header']
                for n in range(procs):
                    edge_file_fragments.append(edge_file+'_'+str(n))
                platform_cat(edge_file_fragments, edge_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

            if qual_file:
                print('Combining the qualifier file fragments', file=sys.stderr, flush=True)
                qual_file_fragments=[qual_file+'_header']
                for n in range(procs):
                    qual_file_fragments.append(qual_file+'_'+str(n))
                platform_cat(qual_file_fragments, qual_file, remove=not keep_temp_files, use_python_cat=use_python_cat, verbose=True)

        print('import complete', file=sys.stderr, flush=True)
        end=time.time()
        print('time taken : {}s'.format(end-start), file=sys.stderr, flush=True)
    except Exception as e:
        raise KGTKException(str(e))
