"""
Import WordNet to KGTK.

"""

import sys
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import WordNet into KGTK.' 
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
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import json
    import nltk
    nltk.download("wordnet")
    from nltk.corpus import wordnet as wn
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkwriter import KgtkWriter

    def obtain_wordnet_lemmas(syn):
        lemmas=[]
        for lemma in syn.lemma_names():
            lemmas.append(KgtkFormat.stringify(lemma.replace('_', ' ')))
        return lemmas

    def obtain_hypernyms(syn):
        hyps=[]
        for hypernym in syn.hypernyms():
            hyps.append(hypernym.name())
        return hyps

    def obtain_member_holonyms(syn):
        hols=[]
        for hol in syn.member_holonyms():
            hols.append(hol.name())
        return hols

    def obtain_part_holonyms(syn):
        hols=[]
        for hol in syn.part_holonyms():
            hols.append(hol.name())
        return hols

    def obtain_substance_meronyms(syn):
        hols=[]
        for hol in syn.substance_meronyms():
            hols.append(hol.name())
        return hols


    def get_wn_data():
        syns=list(wn.all_synsets())
        all_labels={}
        all_hyps={}
        all_members={}
        all_parts={}
        all_subs={}
        for syn in syns:
            syn_name=syn.name()

            lemmas=obtain_wordnet_lemmas(syn)
            all_labels[syn_name]='|'.join(lemmas)

            hypernyms=obtain_hypernyms(syn)
            if len(hypernyms):
                all_hyps[syn_name]=hypernyms
            
            member_holonyms=obtain_member_holonyms(syn)
            if len(member_holonyms):
                all_members[syn_name]=member_holonyms

            part_holonyms=obtain_part_holonyms(syn)
            if len(part_holonyms):
                all_parts[syn_name]=part_holonyms

            substance_meronyms=obtain_substance_meronyms(syn)
            if len(substance_meronyms):
                all_subs[syn_name]=substance_meronyms

        return all_labels, all_hyps, all_members, all_parts, all_subs

    def create_edges(data, labels, rel, rel_label):
        all_rows=[]
        source=KgtkFormat.stringify('WN')
        for node1, v in data.items():
            for node2 in v:
                node1_preflabel=labels[node1].split('|')[0]
                node2_preflabel=labels[node2].split('|')[0]
                a_row=['wn:' + node1, rel, 'wn:' + node2, labels[node1], labels[node2], rel_label, "", source, '']
                all_rows.append(a_row)
        return all_rows

    try:
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

        all_labels, all_hyps, all_members, all_parts, all_subs=get_wn_data()
        hyp_edges=create_edges(all_hyps, all_labels, '/r/IsA', KgtkFormat.stringify('is a'))
        member_edges=create_edges(all_members, all_labels, '/r/PartOf', KgtkFormat.stringify('is a part of'))
        part_edges=create_edges(all_parts, all_labels, '/r/PartOf', KgtkFormat.stringify('is a part of'))
        sub_edges=create_edges(all_subs, all_labels, '/r/MadeOf', KgtkFormat.stringify('is made of'))
        all_edges=hyp_edges+member_edges+part_edges+sub_edges

        for edge in all_edges:
            ew.write(edge)

        # Clean up.
        ew.close()

    except Exception as e:
            kgtk_exception_auto_handler(e)
