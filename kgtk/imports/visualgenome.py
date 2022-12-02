from kgtk.exceptions import KGTKException
import json
from pathlib import Path
from collections import defaultdict
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter


class ImportVisualGenome(object):
    def __init__(self,
                 input_file: Path,
                 attr_syn_file: Path,
                 output_kgtk_file: Path):

        self.input_file = input_file
        self.attr_syn_file = attr_syn_file
        self.output_kgtk_file = output_kgtk_file

    def process(self):
        try:

            out_columns = ['node1', 'relation', 'node2', 'node1;label', 'node2;label', 'relation;label',
                           'relation;dimension', 'source', 'sentence']

            ew: KgtkWriter = KgtkWriter.open(out_columns,
                                             self.output_kgtk_file,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=True,
                                             gzip_in_parallel=False
                                             )

            proximity_relation = '/r/LocatedNear'
            property_relation = 'mw:MayHaveProperty'
            property_relation_label = KgtkFormat.stringify('may have property')
            capableof_relation = '/r/CapableOf'
            capableof_relation_label = KgtkFormat.stringify('capable of')

            with open(self.input_file, 'r') as f:
                images_data = json.load(f)

            with open(self.attr_syn_file, 'r') as f:
                attr_synsets = json.load(f)

            for counter, an_image in enumerate(images_data):

                image_id = str(an_image['image_id'])

                # OBJECTS
                objid2names = defaultdict(list)
                objid2syns = {}
                rows = []
                for o in an_image['objects']:
                    obj_id = o['object_id']
                    o_synset = o['synsets']
                    objid2syns[obj_id] = o_synset
                    for name in o['names']:
                        name = name.strip().lower().rstrip('.')
                        if not name:
                            continue
                        objid2names[obj_id].append(KgtkFormat.stringify(name))

                    # ATTRIBUTES
                    if 'attributes' in o.keys():
                        for attr in o['attributes']:
                            attr = attr.lower()
                            if attr in attr_synsets:
                                asyn = attr_synsets[attr]
                                apos = asyn.split('.')[1]
                                if apos != 'n':
                                    if apos == 'v':  # verb
                                        for osyn in o_synset:
                                            if osyn != asyn:
                                                edge_row = self.create_edge('wn:' + osyn,
                                                                            objid2names[obj_id],
                                                                            'wn:' + asyn,
                                                                            [KgtkFormat.stringify(attr)],
                                                                            capableof_relation,
                                                                            capableof_relation_label,
                                                                            image_id)
                                                if edge_row not in rows:
                                                    rows.append(edge_row)
                                    else:  # adjective
                                        for osyn in o_synset:
                                            if osyn != asyn:
                                                edge_row = self.create_edge('wn:' + osyn,
                                                                            objid2names[obj_id],
                                                                            'wn:' + asyn,
                                                                            [KgtkFormat.stringify(attr)],
                                                                            property_relation,
                                                                            property_relation_label,
                                                                            image_id)
                                                if edge_row not in rows:
                                                    rows.append(edge_row)

                # RELATIONS
                for rel in an_image['relationships']:
                    # synsets=rel['synsets']
                    relation_label = KgtkFormat.stringify(rel['predicate'].lower().strip().strip('.'))
                    sub_id = rel['subject_id']
                    sub_names = objid2names[sub_id]
                    sub_syns = objid2syns[sub_id]
                    obj_id = rel['object_id']
                    obj_names = objid2names[obj_id]
                    obj_syns = objid2syns[obj_id]

                    for ssyn in sub_syns:
                        for osyn in obj_syns:
                            if osyn != ssyn:
                                edge_row = self.create_edge('wn:' + ssyn,
                                                            sub_names,
                                                            'wn:' + osyn,
                                                            obj_names,
                                                            proximity_relation,
                                                            relation_label,
                                                            image_id)
                                if edge_row not in rows:
                                    rows.append(edge_row)
                for a_row in rows:
                    ew.write(a_row)

            # Clean up
            ew.close()

        except Exception as e:
            raise KGTKException(e)

    @staticmethod
    def create_edge(node1, node1_lbl, node2, node2_lbl, rel, rel_lbl, image_id):
        my_row = [node1, rel, node2, '|'.join(node1_lbl), '|'.join(node2_lbl), rel_lbl, '', KgtkFormat.stringify('VG'),
                  '']
        return my_row
