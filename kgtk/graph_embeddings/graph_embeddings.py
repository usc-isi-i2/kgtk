"""
Generate graph embedding based on Pytorch BigGraph library

"""

import shutil
from torchbiggraph.config import parse_config  # type: ignore
from kgtk.exceptions import KGTKException
# copy  missing file under kgtk/graph_embeddings
from kgtk.graph_embeddings.importers import TSVEdgelistReader, convert_input_data
from torchbiggraph.train import train  # type: ignore
from torchbiggraph.util import SubprocessInitializer, setup_logging  # type: ignore
from kgtk.graph_embeddings.export_to_tsv import make_tsv
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
import attr
import typing
from kgtk.kgtkformat import KgtkFormat
from pathlib import Path
import sys
import logging
import os

# remove the Issue: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized.
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


@attr.s(slots=True, frozen=False)
class KgtkCreateTmpTsv(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reader_options: typing.Optional[KgtkReaderOptions] = attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process(self):
        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % str(self.input_file_path), file=self.error_file, flush=True)

        kr: KgtkReader = KgtkReader.open(self.input_file_path,
                                         error_file=self.error_file,
                                         options=self.reader_options,
                                         value_options=self.value_options,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
                                         )

        if self.verbose:
            print("Opening the output file: %s" % str(self.output_file_path), file=self.error_file, flush=True)

        # Open the output file.
        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)
        # here kw has one line already where PBG doesn't need it,

        input_line_count: int = 0
        if self.verbose:
            print("Processing the input records.", file=self.error_file, flush=True)

        # node1 relation node2
        node1_index = kr.get_node1_column_index()
        node2_index = kr.get_node2_column_index()
        relation_index = kr.get_label_column_index()

        row: typing.List[str]

        for row in kr:
            input_line_count += 1
            kw.write([row[node1_index], row[relation_index], row[node2_index]])

        if self.verbose:
            print("Processed %d records." % input_line_count, file=self.error_file, flush=True)

        kw.close()


class ComputeGraphEmbeddings(object):

    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 temporary_directory: Path,
                 output_format: str = 'w2v',
                 retain_temporary_data: bool = True,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 log_file_path: str = None,
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 error_file: typing.TextIO = sys.stderr,
                 operator: str = 'ComplEx',
                 dynamic_relations: bool = True,
                 dimension_num: int = 100,
                 global_emb: bool = False,
                 comparator: str = 'dot',
                 init_scale: float = 0.001,
                 bias: bool = False,
                 num_epochs: int = 100,
                 loss_fn: str = None,
                 learning_rate: float = None,
                 eval_fraction: float = 0.0,
                 output_no_header: bool = False
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.temporary_directory = temporary_directory
        self.output_format = output_format
        self.retain_temporary_data = retain_temporary_data
        self.verbose = verbose
        self.very_verbose = very_verbose
        self.log_file_path = log_file_path
        self.reader_options = reader_options
        self.value_options = value_options
        self.error_file = error_file
        self.operator = operator
        self.dynamic_relations = dynamic_relations
        self.dimension_num = dimension_num
        self.global_emb = global_emb
        self.comparator = comparator
        self.init_scale = init_scale
        self.bias = bias
        self.num_epochs = num_epochs
        self.loss_fn = loss_fn
        self.learning_rate = learning_rate
        self.eval_fraction = eval_fraction
        self.output_no_header = output_no_header

    def get_config(self):
        """
        configurations for graph embedding
        """

        output_folder: Path = self.temporary_directory / 'output'
        entity_path = str(output_folder)
        edge_paths = [str((output_folder / 'edges_partitioned'))]
        checkpoint_path = str((output_folder / 'model'))

        config = dict(
            # I/O data
            entity_path=entity_path,
            edge_paths=edge_paths,
            checkpoint_path=checkpoint_path,
            # Graph structure
            entities={"all": {"num_partitions": 1}},
            relations=[  # relation template setting
                {
                    "name": "all_edges",
                    "lhs": "all",
                    "rhs": "all",
                    "operator": self.operator,
                }
            ],
            dynamic_relations=self.dynamic_relations,
            # Scoring model
            dimension=self.dimension_num,
            global_emb=self.global_emb,
            comparator=self.comparator,
            # Training
            init_scale=self.init_scale,
            bias=self.bias,
            num_epochs=self.num_epochs,
            loss_fn=self.loss_fn,
            lr=self.learning_rate,
            # Evaluation during training
            eval_fraction=self.eval_fraction,  # to reproduce results, we need to use all training data
        )

        return config

    @staticmethod
    def config_preprocess(raw_config):
        # Setting learning rate and loss function for different algo if user doesn't assign them
        '''
        loss_fn: ranking
        learning_rate: 0.01
        operator:complex_diagonal
        '''

        algorithm_operator = {"complex": "complex_diagonal",
                              "distmult": "diagonal",
                              "rescal": "linear",
                              "transe": "translation"}
        try:
            algorithm = algorithm_operator[raw_config['relations'][0]['operator'].lower()]
            raw_config['relations'][0]['operator'] = algorithm
        except Exception:
            print('Plase use valid operator! choices: RESCAL|DistMult|ComplEx|TransE', file=sys.stderr, flush=True)
            sys.exit()

        loss_fn = raw_config['loss_fn']
        learning_rate = raw_config['lr']
        if algorithm and loss_fn and learning_rate:
            return

        if not algorithm:  # use doesn't enter anything
            raw_config['relations'][0]['operator'] = 'complex_diagonal'
            if not loss_fn:
                raw_config['loss_fn'] = 'logistic'
            if not learning_rate:
                raw_config['lr'] = 0.1
        if algorithm:  # give the algorithm
            if algorithm == 'complex_diagonal':  # ComplEx
                if not loss_fn:
                    raw_config['loss_fn'] = 'logistic'
                if not learning_rate:
                    raw_config['lr'] = 0.1
            elif algorithm == 'translation':  # TransE
                if not loss_fn:
                    raw_config['loss_fn'] = 'logistic'
                if not learning_rate:
                    raw_config['lr'] = 0.1
            elif algorithm == 'diagonal':  # DistMult
                if not loss_fn:
                    raw_config['loss_fn'] = 'ranking'
                if not learning_rate:
                    raw_config['lr'] = 0.01
            else:  # RESCAL
                if not loss_fn:
                    raw_config['loss_fn'] = 'ranking'
                if not learning_rate:
                    raw_config['lr'] = 0.01

        processed_config = raw_config
        return processed_config

    # convert wv format to kgtk format ..
    def generate_kgtk_output(self, entities_output, output_no_header):
        # Open the output file.
        kw: KgtkWriter = KgtkWriter.open(
            ['node1', 'label', 'node2'],
            self.output_kgtk_file,
            mode=KgtkWriter.Mode.AUTO,
            require_all_columns=False,
            prohibit_extra_columns=False,
            fill_missing_columns=False,
            gzip_in_parallel=False,
            no_header=output_no_header,
            verbose=self.verbose,
            very_verbose=self.very_verbose)

        input_line_count: int = 0
        if self.verbose:
            logging.info("Processing the input records.", file=self.error_file, flush=True)

        module_name = 'graph_embeddings'  # __name__.split('.')[-1]
        with open(entities_output) as wv_file:
            for line in wv_file:
                vals = line.strip().split('\t')
                entity_name = vals[0]
                entity_vev = ','.join(vals[1:])
                input_line_count += 1
                kw.write([entity_name, module_name, entity_vev])

        if self.verbose:
            logging.info("Processed %d records." % input_line_count, file=self.error_file, flush=True)

        kw.close()

    def generate_w2v_output(self, entities_output):
        fout = open(self.output_kgtk_file, 'w')
        fin = open(entities_output)
        entity_num = len(fin.readlines())
        fin.close()
        fout.write(str(entity_num) + ' ' + str(self.dimension_num) + '\n')
        with open(entities_output) as fin:
            for line in fin:
                embedding = ' '.join(line.split('\t'))
                fout.write(embedding)
        fout.close()

    def process(self):

        try:

            # store the data into log file, then the console will not output anything
            if self.log_file_path is not None:
                logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] \
                - %(levelname)s: %(message)s',
                                    level=logging.DEBUG,
                                    filename=str(self.log_file_path),
                                    filemode='w')
                print(f'In Processing, Please go to {self.log_file_path} to check details', file=sys.stderr,
                      flush=True)

            tmp_tsv_path: Path = self.temporary_directory / f'tmp_{self.input_kgtk_file.name}'

            #  make sure the tmp folder exists, otherwise it will raise an exception
            if not os.path.exists(self.temporary_directory):
                os.makedirs(self.temporary_directory)

            try:  # if output_kgtk_file is not empty, delete it
                self.output_kgtk_file.unlink()
            except Exception:
                pass  # didn't find, then let it go

            # *********************************************
            # 0. PREPARE PBG TSV FILE
            # *********************************************
            kct: KgtkCreateTmpTsv = KgtkCreateTmpTsv(input_file_path=self.input_kgtk_file,
                                                     output_file_path=tmp_tsv_path,
                                                     reader_options=self.reader_options,
                                                     value_options=self.value_options,
                                                     error_file=self.error_file,
                                                     verbose=self.verbose,
                                                     very_verbose=self.very_verbose,
                                                     )
            # prepare the graph file
            # create a tmp tsv file for PBG embedding

            logging.info('Generate the valid tsv format for embedding ...')
            kct.process()
            logging.info('Embedding file is ready...')

            # *********************************************
            # 1. DEFINE CONFIG
            # *********************************************
            raw_config = self.get_config()

            # setting corresponding learning rate and loss function for different algorthim
            processed_config = self.config_preprocess(raw_config)

            # temporry output folder
            tmp_output_folder = Path(processed_config['entity_path'])

            # before moving, need to check whether the tmp folder is not empty in case of bug
            try:  # if temporary output folder is alrady existing then delete it
                shutil.rmtree(tmp_output_folder)
            except Exception:
                pass  # didn't find, then let it go

            # **************************************************
            # 2. TRANSFORM GRAPH TO A BIGGRAPH-FRIENDLY FORMAT
            # **************************************************
            setup_logging()
            config = parse_config(processed_config)
            subprocess_init = SubprocessInitializer()
            input_edge_paths = [tmp_tsv_path]

            convert_input_data(
                config.entities,
                config.relations,
                config.entity_path,
                config.edge_paths,
                input_edge_paths,
                TSVEdgelistReader(lhs_col=0, rel_col=1, rhs_col=2),
                dynamic_relations=config.dynamic_relations,
            )

            # ************************************************
            # 3. TRAIN THE EMBEDDINGS
            # *************************************************
            train(config, subprocess_init=subprocess_init)

            # ************************************************
            # 4. GENERATE THE OUTPUT
            # ************************************************
            # entities_output = output_kgtk_file
            entities_output = tmp_output_folder / 'entities_output.tsv'
            relation_types_output = tmp_output_folder / 'relation_types_tf.tsv'

            with open(entities_output, "xt") as entities_tf, open(
                    relation_types_output, "xt"
            ) as relation_types_tf:
                make_tsv(config, entities_tf, relation_types_tf)

            # output  correct format for embeddings
            if self.output_format == 'glove':  # glove format output
                shutil.copyfile(entities_output, self.output_kgtk_file)
            elif self.output_format == 'w2v':  # w2v format output
                self.generate_w2v_output(entities_output)

            else:  # write to the kgtk output format tsv
                self.generate_kgtk_output(entities_output,
                                          self.output_no_header
                                          )

            logging.info(f'Embeddings has been generated in {self.output_kgtk_file}.')

            # ************************************************
            # 5. Garbage collection
            # ************************************************
            if not self.retain_temporary_data:
                shutil.rmtree(self.temporary_directory)
                # tmp_tsv_path.unlink() # delete temporay tsv file
                # shutil.rmtree(tmp_output_folder) # deleter temporay output folder

            if self.log_file_path is not None:
                print('Processed Finished.', file=sys.stderr, flush=True)
                logging.info(f"Process Finished.\nOutput has been saved in {repr(str(self.output_kgtk_file))}")
            else:
                print(f"Process Finished.\nOutput has been saved in {repr(str(self.output_kgtk_file))}",
                      file=sys.stderr, flush=True)

        except Exception as e:
            raise KGTKException(str(e))
