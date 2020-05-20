"""
Import ConceptNet file to KGTK.
"""


import sys

def parser():
    return {
        'help': 'Import ConceptNet into KGTK.' 
    }


def add_arguments(parser):
	"""
	Parse arguments
	Args:
		parser (argparse.ArgumentParser)
	"""
	# '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
	parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='filename here')
	parser.add_argument('--english_only', action="store_true", help="Only english conceptnet?")
	parser.add_argument('--sort', action="store_true", help="Should we sort the file on s-p-o?")


def run(filename, english_only, sort):
	# import modules locally
	import sys # type: ignore
	from kgtk.exceptions import kgtk_exception_auto_handler
	import pandas as pd

	try:
		df=pd.read_csv(filename, sep='\t', header=None)
		df.columns=['assertion','rel','subj','obj','metadata']
		df.drop(columns=['assertion', 'metadata'], inplace=True)
		df=df[['subj', 'rel', 'obj']]
		df.columns=['node1', 'label', 'node2']

		if sort:
			df=df.sort_values(by=['node1', 'label','node2'])

		# writing of the output
		sys.stdout.write('node1\tlabel\tnode2\n')
		for i, row in df.iterrows():
			if not english_only or (row[0].startswith('/c/en/') and row[2].startswith('/c/en/')):
				sys.stdout.write('%s\n' % '\t'.join(row))


	except Exception as e:
		kgtk_exception_auto_handler(e)
