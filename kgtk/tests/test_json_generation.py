import unittest
import os
from kgtk.generator import JsonGenerator
from pathlib import Path

class TestTripleGeneration(unittest.TestCase):
    def test_dates_generation(self):
        # to reproduce standard file in the `data` folder
        # cat dates.tsv | kgtk generate-mediawiki-jsons -n 100 -pf wikidata_properties.tsv -pr dates 
        dates_tsv_file = 'data/dates.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        generator = JsonGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliase',
                                    description_set='description', warning=True, n=100,
                                    log_path="data/date_warning.log",
                                    has_rank=False,
                                    prop_declaration=False, 
                                    output_prefix="data/dates_tmp")
        fp = open(dates_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        fp.close()

        f1 = open('data/dates0.jsonl')
        f2 = open('data/dates_tmp0.jsonl')
        self.assertEqual(f1.readlines(), f2.readlines()) 
        #TODO until date validation published
        # self.assertEqual(f1.readlines(), f2.readlines()) 
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/date_warning.log").st_size, 0)
        p = Path("data/date_warning.log")
        p.unlink()
        p = Path('data/dates_tmp0.jsonl')
        p.unlink()

    def test_property_json_generation(self):
        # to reproduce standard file in the `data` folder
        # cat P10.tsv | kgtk generate-mediawiki-jsons -n 100 -pf wikidata_properties.tsv -pr P10 -ap aliases -dp descriptions
        property_tsv_file = 'data/P10.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        generator = JsonGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=1000,
                                    log_path="data/P10_warning.log",
                                    has_rank = False,
                                    prop_declaration=False, 
                                    output_prefix="data/P10_tmp")
        fp = open(property_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        fp.close()
        f1 = open('data/P100.jsonl')
        f2 = open('data/P10_tmp0.jsonl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/P10_warning.log").st_size, 0)
        p = Path("data/P10_warning.log")
        p.unlink()
        p = Path('data/P10_tmp0.jsonl')
        p.unlink()

    def test_qnode_json_generation(self):
        # to reproduce standard file in the `data` folder
        # cat Q57160439.tsv | kgtk generate-mediawiki-jsons -n 100 -pf wikidata_properties.tsv -pr Q57160439 -ap aliases -dp descriptions
        qnode_tsv_file = 'data/Q57160439.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        generator = JsonGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=1000,
                                    log_path="data/Q57160439_warning.log",
                                    prop_declaration=False, 
                                    has_rank = False,
                                    output_prefix="data/Q57160439_tmp")
        fp = open(qnode_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        fp.close()
        f1 = open('data/Q571604390.jsonl')
        f2 = open('data/Q57160439_tmp0.jsonl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/Q57160439_warning.log").st_size, 0)
        p = Path("data/Q57160439_warning.log")
        p.unlink()
        p = Path('data/Q57160439_tmp0.jsonl')
        p.unlink()

    def test_ranked_kgtk_generation(self):
        # to reproduce standard file in the `data` folder
        # kgtk generate_mediawiki_jsons -i ranked_example.tsv --debug -pf wikidata_properties.tsv -pr ranked
        ranked_tsv_file = 'data/ranked_example.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        generator = JsonGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='alias',
                                    description_set='description', warning=True, n=1000,
                                    log_path="data/ranked_warning.log",
                                    prop_declaration=False, 
                                    has_rank = False,
                                    output_prefix="data/ranked_tmp")
        fp = open(ranked_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        fp.close()
        f1 = open('data/ranked0.jsonl')
        f2 = open('data/ranked_tmp0.jsonl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path('data/ranked_tmp0.jsonl')
        p.unlink()