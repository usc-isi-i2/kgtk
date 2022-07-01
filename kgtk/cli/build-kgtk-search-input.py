import traceback
from kgtk.exceptions import KGTKException


def parser():
    return {
        'help': 'builds a json lines file to be loaded into elasticsearch from a kgtk edge file.'
    }


def add_arguments(parser):
    """
    Parse Arguments
    Args:
        parser: (argparse.ArgumentParser)

    """

    parser.add_argument('--label-properties', action='store', type=str, dest='label_properties', required=True,
                        help='the name of property which has labels for the node1')

    parser.add_argument('--alias-properties', action='store', type=str, dest='alias_properties', default=None,
                        help='the name of property which has aliases for the node1')

    parser.add_argument('--extra-alias-properties', action='store', type=str, dest='extra_alias_properties',
                        default="P1448,P1705,P1477,P1810",
                        help='comma separated list of properties to be used as additional aliases.')
    # P1448: official name
    # P1705: native label
    # P1477: official name
    # P1810: named as

    parser.add_argument('--description-properties', action='store', type=str, dest='description_properties',
                        default=None,
                        help='the name of property which has descriptions for the node1')

    parser.add_argument('--pagerank-properties', action='store', type=str, dest='pagerank_properties', default=None,
                        help='the name of property which has pagerank for the node1')

    parser.add_argument('--mapping-file', action='store', dest='mapping_file_path', required=True,
                        help='path where a mapping file for the ES index will be output')

    parser.add_argument('--add-text', action='store_true', dest='add_text', default=False,
                        help='add a text field in the json which contains all text in label, alias and description')

    parser.add_argument('--input-file', action='store', dest='input_file_path', required=True,
                        help='input kgtk edge file, sorted by node1')

    parser.add_argument('--output-file', action='store', dest='output_file_path', required=True,
                        help='output json lines file, to be loaded into ES')

    parser.add_argument('--property-datatype-file', action='store', dest='property_datatype_file', default=None,
                        help='A file in KGTK edge file format with data types for properties')
    parser.add_argument('--languages', action='store', type=str, dest='languages',
                        default="en",
                        help='a comma separated list of languages for labels, aliases and descriptions')


def run(**kwargs):
    from kgtk.utils.elasticsearch_manager import ElasticsearchManager
    languages = set(kwargs['languages'].split(","))
    try:

        ElasticsearchManager.build_kgtk_search_input(kwargs['input_file_path'], kwargs['label_properties'],
                                                     kwargs['mapping_file_path'], kwargs['output_file_path'],
                                                     alias_fields=kwargs['alias_properties'],
                                                     extra_alias_properties=kwargs['extra_alias_properties'],
                                                     pagerank_fields=kwargs['pagerank_properties'],
                                                     description_properties=kwargs['description_properties'],
                                                     add_text=kwargs['add_text'],
                                                     property_datatype_file=kwargs['property_datatype_file'],
                                                     languages=languages
                                                     )
    except:
        message = 'Command: build-kgtk-search-input\n'
        message += 'Error Message:  {}\n'.format(traceback.format_exc())
        raise KGTKException(message)
