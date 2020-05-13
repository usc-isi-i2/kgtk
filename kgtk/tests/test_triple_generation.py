import unittest
from kgtk.triple_generator import TripleGenerator
from pathlib import Path


class TestTripleGeneration(unittest.TestCase):

    def test_truthy_property_triple_generation(self):
        property_tsv_file = 'data/P10.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/P10_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', ignore=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o)
        for line_num, edge in enumerate(open(property_tsv_file)):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        o.close()
        f1 = open('data/P10_truthy.ttl')
        f2 = open('data/P10_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path('data/P10_truthy_tmp.ttl')
        p.unlink()

    def test_property_triple_generation(self):
        property_tsv_file = 'data/P10.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/P10_not_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', ignore=True, n=100, truthy=False, use_id=True,
                                    dest_fp=o)
        for line_num, edge in enumerate(open(property_tsv_file)):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()
        o.close()
        f1 = open('data/P10_not_truthy.ttl')
        f2 = open('data/P10_not_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path('data/P10_not_truthy_tmp.ttl')
        p.unlink()

    def test_truthy_qnode_triple_generation(self):
        qnode_tsv_file = 'data/Q57160439.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/Q57160439_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', ignore=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o)
        for line_num, edge in enumerate(open(qnode_tsv_file)):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()

        o.close()

        f1 = open('data/Q57160439_truthy.ttl')
        f2 = open('data/Q57160439_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path('data/Q57160439_truthy_tmp.ttl')
        p.unlink()

    def test_not_truthy_qnode_triple_generation(self):
        qnode_tsv_file = 'data/Q57160439.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/Q57160439_not_truthy_tmp.ttl', 'w')
        generator = TripleGenerator(wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', ignore=True, n=100, truthy=False, use_id=True,
                                    dest_fp=o)
        for line_num, edge in enumerate(open(qnode_tsv_file)):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()

        o.close()
        f1 = open('data/Q57160439_not_truthy.ttl')
        f2 = open('data/Q57160439_not_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path('data/Q57160439_not_truthy_tmp.ttl')
        p.unlink()

    def test_triple_small_values(self):
        small_values_file = 'data/small_values.tsv'
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = open('data/small_values_tmp.ttl', 'w')
        generator = TripleGenerator(wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', ignore=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o)
        for line_num, edge in enumerate(open(small_values_file)):
            if edge.startswith("#"):
                continue
            else:
                generator.entry_point(line_num + 1, edge)
        generator.finalize()

        o.close()

        f1 = open('data/small_values.ttl')
        f2 = open('data/small_values_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path('data/small_values_tmp.ttl')
        p.unlink()