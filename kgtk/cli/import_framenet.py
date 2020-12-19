"""
Import FrameNet to KGTK.
"""


import sys
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import FrameNet into KGTK.' 
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_output_file()

def run(output_file: KGTKFiles):
    # import modules locally

    from typing import Tuple, List, Union, Dict
    import nltk
    import pandas as pd
    nltk.download('framenet_v17')
    from nltk.corpus import framenet as fn
    import re
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkwriter import KgtkWriter

    def edge2KGTK(edge: Tuple[str, str, str]) -> pd.Series:
        """
        Gets the edge as triple of subject, object, predicate and converts the edge to the KGTK format
        Args:
            edge: Tuple[str, str, str]
                input edge
        Returns: pd.Series
            pandas Series with keys according to KGTK format at
            https://docs.google.com/document/d/1fbbqgyX0N2EdxLam6hatfke1R-nZWkoN6M1oB_f4aQo/edit#heading=h.a5nlqev5bmm4
        """
        s, p, o = edge

        def clean(e: str) -> str:
            out = e.split(':')[-1].replace('_', ' ')
            return KgtkFormat.stringify(re.sub("([a-z])([A-Z])", "\g<1> \g<2>", out).strip().lower())

        return pd.Series({
            'node1': s,
            'relation': p,
            'node2': o,
            'node1;label': clean(s),
            'node2;label': clean(o),
            'relation;label': clean(p),
            'relation;dimension': '',
            'source': KgtkFormat.stringify('FN'),
            'sentence': ''
        })

    def load_framenet():
        edges=[]
        for frm in fn.frames():
            # frame-frame relations
            for fe in frm.frameRelations:
                edges=pretty_frame_edge(edges, frm_id(fe.superFrameName),
                               frm_id(fe.subFrameName), ncheck(fe.type.name))

            # lexical units
            for lu in frm.lexUnit.keys():
                edges.append([frm_id(frm.name), 'fn:HasLexicalUnit', lu_format(lu, frm.name)])

            # FE
            for fe in frm.FE.values():
                if isinstance(fe.semType, nltk.corpus.reader.framenet.AttrDict):

                    # Sem type
                    semtype_edge=[fe_id(fe.name),
                                    '/r/IsA', #'fn:HasSemType',
                                   fe_semtype_id(fe.semType.name)]
                    if semtype_edge not in edges:
                        edges.append(semtype_edge)


                    # Root type
                    root_edge=[fe_semtype_id(fe.semType.name),
                                    '/r/IsA', # 'fn:st:RootType'
                                   fe_semtype_id(fe.semType.rootType.name)]
                    if root_edge not in edges:
                        edges.append(root_edge)


                    # Super type
                    super_edge=[fe_semtype_id(fe.semType.name),
                                    '/r/IsA', #'fn:st:SuperType',
                                   fe_semtype_id(fe.semType.superType.name)]
                    if super_edge not in edges:
                        edges.append(super_edge)


                    # Sub type
                    for fesub in fe.semType.subTypes:
                        sub_edge=[fe_semtype_id(fesub.name),
                                    '/r/IsA',
                                    fe_semtype_id(fe.semType.name)]
                        if sub_edge not in edges:
                            edges.append(sub_edge)
                        #edges.append([fe_semtype_id(fe.semType.name),
                        #            'fn:st:SubType',
                        #            fe_semtype_id(fesub.name)])


                # Requires FE
                if isinstance(fe.requiresFE, nltk.corpus.reader.framenet.AttrDict):
                    req_edge=[fe_id(fe.name), '/r/HasPrerequisite', fe_id(fe.requiresFE.name)]
                    if req_edge not in edges:
                        edges.append(req_edge)
                    #edges.append([fe_id(fe.name), 'fn:fe:RequiresFE', fe_id(fe.requiresFE.name)])

                # Excludes FE
                if isinstance(fe.excludesFE, nltk.corpus.reader.framenet.AttrDict):
                    excl_edge=[fe_id(fe.name), '/r/RelatedTo', fe_id(fe.excludesFE.name)]
                    if excl_edge not in edges:
                        edges.append(excl_edge)
                    #edges.append([fe_id(fe.name), 'fn:fe:ExcludesFE', fe_id(fe.excludesFE.name)])

                # HasFrameElement - coreType as edge feature
                hasfe_edge=[frm_id(frm.name),
                            '/r/HasA', #'fn:HasFrameElement',
                            fe_id(fe.name)]
                if hasfe_edge not in edges:
                    edges.append(hasfe_edge)
        return edges

    def nosp(s):
        return s.replace(' ', '_').split('.')[0].lower()


    def lu_format(wn: str, _fn: str = "") -> str:
        return f'fn:lu:{nosp(_fn)}:{nosp(wn)}'


    def frm_id(me: str) -> str:
        return f'fn:{nosp(me)}'


    def fe_id(fe: str) -> str:
        return f'fn:fe:{nosp(fe)}'


    def fe_semtype_id(sem: str) -> str:
        return f'fn:st:{nosp(sem)}'


    def ncheck(e):
        if e is None:
            return ""
        elif isinstance(e, nltk.corpus.reader.framenet.AttrDict):
            return e
        else:
            return e


    def pretty_frame_edge(edges, s, o, p):
        pn = nosp(p)
        if pn == 'inheritance':
            edges.append([o, '/r/IsA', s])
        elif pn == 'using':
            edges.append([s, '/r/UsedFor', o])
        elif pn == 'subframe':
            edges.append([s, '/r/HasSubevent', o])
        elif pn == 'precedes':
            edges.append([o, '/r/HasPrerequisite', s])
        elif pn == 'perspective_on':
            edges.append([o, '/r/IsA', s])
        else:
            name = {
                'is_inchoative_of': '/r/Causes',
                'inchoative_of': '/r/Causes',
                #
                'is_causative_of': '/r/Causes',
                'causative_of': '/r/Causes',
                #
                'see_also': '/r/RelatedTo',
                #
                'reframing_mapping': '/r/SimilarTo',
                'metaphor': '/r/SimilarTo',
            }[pn]
            edges.append([s, name, o])
        return edges

    try:
        edges=load_framenet()
        out_columns=['node1', 'relation', 'node2', 'node1;label', 'node2;label','relation;label', 'relation;dimension', 'source', 'sentence']

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
        ew: KgtkWriter = KgtkWriter.open(out_columns,
                                         output_kgtk_file,
                                         #mode=input_kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         #verbose=self.verbose,
                                         #very_verbose=self.very_verbose
                                         )
        df_ = pd.DataFrame(map(edge2KGTK, edges))

        for i, row in df_.iterrows():
            ew.write(row)

        ew.close()

    except Exception as e:
            kgtk_exception_auto_handler(e)
