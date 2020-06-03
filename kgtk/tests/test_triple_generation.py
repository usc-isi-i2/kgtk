import unittest
import os
from kgtk.generator import TripleGenerator
from pathlib import Path


class TestTripleGeneration(unittest.TestCase):

    def test_truthy_property_triple_generation(self):
        property_tsv_file = 'data/P10.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/P10_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o,log_path="data/warning.log",prop_declaration=False)
        fp = open(property_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        o.close()
        fp.close()
        f1 = open('data/P10_truthy.ttl')
        f2 = open('data/P10_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/P10_truthy_tmp.ttl')
        p.unlink()

    def test_property_triple_generation(self):
        property_tsv_file = 'data/P10.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/P10_not_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=False, use_id=True,
                                    dest_fp=o,log_path="data/warning.log",prop_declaration=False)
        fp = open(property_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        fp.close()
        o.close()
        f1 = open('data/P10_not_truthy.ttl')
        f2 = open('data/P10_not_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/P10_not_truthy_tmp.ttl')
        p.unlink()

    def test_truthy_qnode_triple_generation(self):
        qnode_tsv_file = 'data/Q57160439.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/Q57160439_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o,log_path="data/warning.log",prop_declaration=False)
        fp = open(qnode_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        o.close()
        fp.close()
        f1 = open('data/Q57160439_truthy.ttl')
        f2 = open('data/Q57160439_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/Q57160439_truthy_tmp.ttl')
        p.unlink()

    def test_not_truthy_qnode_triple_generation(self):
        qnode_tsv_file = 'data/Q57160439.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/Q57160439_not_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=False, use_id=True,
                                    dest_fp=o,log_path="data/warning.log",prop_declaration=False)
        fp = open(qnode_tsv_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        fp.close()
        o.close()
        f1 = open('data/Q57160439_not_truthy.ttl')
        f2 = open('data/Q57160439_not_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/Q57160439_not_truthy_tmp.ttl')
        p.unlink()

    def test_triple_small_values(self):
        small_values_file = 'data/small_values.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/small_values_tmp.ttl', 'w')
        generator = TripleGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o,log_path="data/warning.log",prop_declaration=False)
        fp = open(small_values_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()

        o.close()
        fp.close()
        f1 = open('data/small_values.ttl')
        f2 = open('data/small_values_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/small_values_tmp.ttl')
        p.unlink()

    def test_triple_corrupted_edges(self):
        corrupted_kgtk_file = 'data/corrupted_kgtk.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/corrupted_tmp.ttl', 'w')
        generator = TripleGenerator(prop_file = wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o,log_path="data/corrupted_warning_tmp.log",prop_declaration=False)
        fp = open(corrupted_kgtk_file)
        for line_num, edge in enumerate(fp):
            if edge.startswith("#") or len(edge.strip("\n")) == 0:
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()

        o.close()
        fp.close()
        f1 = open('data/corrupted.ttl')
        f2 = open('data/corrupted_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        f1 = open("data/corrupted_warning.log")
        f2 = open("data/corrupted_warning_tmp.log")
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path("data/corrupted_warning_tmp.log")
        p.unlink()
        p = Path('data/corrupted_tmp.ttl')
        p.unlink()