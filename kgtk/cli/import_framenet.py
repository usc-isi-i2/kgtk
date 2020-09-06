"""
Import FrameNet to KGTK.
TODO: Add --output-file
"""


import sys

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

def run():
    # import modules locally

    from typing import Tuple, List, Union, Dict
    import nltk
    import pandas as pd
    nltk.download('framenet_v17')
    from nltk.corpus import framenet as fn
    import re
    from kgtk.kgtkformat import KgtkFormat

    def header_to_edge(row):
        row=[r.replace('_', ';') for r in row]
        return '\t'.join(row) + '\n'

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

                    edges.append([fe_id(fe.name),
                                    'fn:HasSemType',
                                   fe_semtype_id(fe.semType.name)])

                    edges.append([fe_semtype_id(fe.semType.name),
                                    'fn:st:RootType',
                                   fe_semtype_id(fe.semType.rootType.name)])

                    edges.append([fe_semtype_id(fe.semType.name),
                                    'fn:st:SuperType',
                                   fe_semtype_id(fe.semType.superType.name)])

                    for fesub in fe.semType.subTypes:
                        edges.append([fe_semtype_id(fe.semType.name),
                                    'fn:st:SubType',
                                    fe_semtype_id(fesub.name)])


                if isinstance(fe.requiresFE, nltk.corpus.reader.framenet.AttrDict):
                    edges.append([fe_id(fe.name), 'fn:fe:RequiresFE', fe_id(fe.requiresFE.name)])

                if isinstance(fe.excludesFE, nltk.corpus.reader.framenet.AttrDict):
                    edges.append([fe_id(fe.name), 'fn:fe:ExcludesFE', fe_id(fe.excludesFE.name)])

                # coreType as edge feature
                edges.append([frm_id(frm.name), 
                            'fn:HasFrameElement',
                            fe_id(fe.name)])
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
            edges.append([s, 'fn:IsInheritedBy', o])
            edges.append([o, 'fn:InheritsFrom', s])
        elif pn == 'using':
            edges.append([s, 'fn:IsUsedBy', o])
            edges.append([o, 'fn:Uses', s])
        elif pn == 'subframe':
            edges.append([s, 'fn:HasSubframe', o])
            edges.append([o, 'fn:SubframeOf', s])
        elif pn == 'precedes':
            edges.append([s, 'fn:Precedes', o])
            edges.append([o, 'fn:IsPrecededBy', s])
        elif pn == 'perspective_on':
            edges.append([s, 'fn:IsPerspectivizedIn', o])
            edges.append([o, 'fn:PerspectiveOn', s])
        else:
            # 'Is Inchoative of:'
            # 'Is Causative of:'
            # 'See also:'
            name = {
                'is_inchoative_of': 'IsInchoativeOf',
                'inchoative_of': 'IsInchoativeOf',
                #
                'is_causative_of': 'IsCausativeOf',
                'causative_of': 'IsCausativeOf',
                #
                'see_also': 'SeeAlso',
                #
                'reframing_mapping': 'ReframingMapping',
                'metaphor': 'Metaphor',
            }[pn]
            edges.append([s, f'fn:{name}', o])
        return edges

    try:
        edges=load_framenet()
        out_columns=['node1', 'relation', 'node2', 'node1_label', 'node2_label','relation_label', 'relation_dimension', 'source', 'sentence']
        sys.stdout.write(header_to_edge(out_columns))

        df_ = pd.DataFrame(map(edge2KGTK, edges))

        for i, row in df_.iterrows():
            sys.stdout.write('\t'.join(row) + '\n')

    except Exception as e:
            kgtk_exception_auto_handler(e)
