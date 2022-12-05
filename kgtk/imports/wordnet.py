from kgtk.exceptions import KGTKException
import nltk
from nltk.corpus import wordnet as wn
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter
from pathlib import Path

nltk.download("wordnet")
nltk.download('omw-1.4')


class ImportWordNet(object):
    def __init__(self,
                 output_kgtk_file: Path):
        self.output_kgtk_file = output_kgtk_file

    @staticmethod
    def obtain_wordnet_lemmas(syn):
        lemmas = []
        for lemma in syn.lemma_names():
            lemmas.append(KgtkFormat.stringify(lemma.replace('_', ' ')))
        return lemmas

    @staticmethod
    def obtain_hypernyms(syn):
        hyps = []
        for hypernym in syn.hypernyms():
            hyps.append(hypernym.name())
        return hyps

    @staticmethod
    def obtain_member_holonyms(syn):
        hols = []
        for hol in syn.member_holonyms():
            hols.append(hol.name())
        return hols

    @staticmethod
    def obtain_part_holonyms(syn):
        hols = []
        for hol in syn.part_holonyms():
            hols.append(hol.name())
        return hols

    @staticmethod
    def obtain_substance_meronyms(syn):
        hols = []
        for hol in syn.substance_meronyms():
            hols.append(hol.name())
        return hols

    @staticmethod
    def get_wn_data():
        syns = list(wn.all_synsets())
        all_labels = {}
        all_hyps = {}
        all_members = {}
        all_parts = {}
        all_subs = {}
        for syn in syns:
            syn_name = syn.name()

            lemmas = ImportWordNet.obtain_wordnet_lemmas(syn)
            all_labels[syn_name] = '|'.join(lemmas)

            hypernyms = ImportWordNet.obtain_hypernyms(syn)
            if len(hypernyms):
                all_hyps[syn_name] = hypernyms

            member_holonyms = ImportWordNet.obtain_member_holonyms(syn)
            if len(member_holonyms):
                all_members[syn_name] = member_holonyms

            part_holonyms = ImportWordNet.obtain_part_holonyms(syn)
            if len(part_holonyms):
                all_parts[syn_name] = part_holonyms

            substance_meronyms = ImportWordNet.obtain_substance_meronyms(syn)
            if len(substance_meronyms):
                all_subs[syn_name] = substance_meronyms

        return all_labels, all_hyps, all_members, all_parts, all_subs

    @staticmethod
    def create_edges(data, labels, rel, rel_label):
        all_rows = []
        source = KgtkFormat.stringify('WN')
        for node1, v in data.items():
            for node2 in v:
                a_row = ['wn:' + node1, rel, 'wn:' + node2, labels[node1], labels[node2], rel_label, "", source, '']
                all_rows.append(a_row)
        return all_rows

    def process(self):

        try:
            out_columns = ['node1', 'relation', 'node2', 'node1;label', 'node2;label', 'relation;label',
                           'relation;dimension', 'source', 'sentence']

            ew: KgtkWriter = KgtkWriter.open(out_columns,
                                             self.output_kgtk_file,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=True,
                                             gzip_in_parallel=False,
                                             # verbose=self.verbose,
                                             # very_verbose=self.very_verbose
                                             )

            all_labels, all_hyps, all_members, all_parts, all_subs = self.get_wn_data()
            hyp_edges = self.create_edges(all_hyps, all_labels, '/r/IsA', KgtkFormat.stringify('is a'))
            member_edges = self.create_edges(all_members, all_labels, '/r/PartOf', KgtkFormat.stringify('is a part of'))
            part_edges = self.create_edges(all_parts, all_labels, '/r/PartOf', KgtkFormat.stringify('is a part of'))
            sub_edges = self.create_edges(all_subs, all_labels, '/r/MadeOf', KgtkFormat.stringify('is made of'))
            all_edges = hyp_edges + member_edges + part_edges + sub_edges

            for edge in all_edges:
                ew.write(edge)

            # Clean up.
            ew.close()

        except Exception as e:
            raise KGTKException(e)
