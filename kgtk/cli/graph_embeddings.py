"""
Generate graph embedding based on Pytorch BigGraph library  

"""

from argparse import Namespace
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
import attr,sys,typing
from kgtk.kgtkformat import KgtkFormat
from pathlib import Path
import sys

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True' # remove the Issue: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized.


@attr.s(slots=True, frozen=False)
class KgtkCreateTmpTsv(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process(self):
        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % str(self.input_file_path), file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
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
        node1_index= kr.get_node1_column_index()
        node2_index = kr.get_node2_column_index()
        ##relation_index = kr.get_id_column_index('relation')#
        relation_index = kr.get_label_column_index()
      
        row: typing.List[str]
        # delete header
        # kw.file_out.seek(0)         # set the cursor to the top of the file
        # kw.file_out.truncate()      # truncate following part == delete first line
        # print(kw.file_out.tell())

        for row in kr:
            input_line_count += 1
            kw.write([row[node1_index],row[relation_index],row[node2_index]]) 
           
        if self.verbose:
            print("Processed %d records." % (input_line_count), file=self.error_file, flush=True)
    
        kw.close()

def get_config(**kwargs): 
    """
    configurations for graph embedding
    """
    # import modules locally
    from pathlib import Path

    output_folder = kwargs['temporary_directory'] / 'output'
    entity_path = str(output_folder)
    edge_paths = [ str((output_folder / 'edges_partitioned')) ]
    checkpoint_path = str((output_folder / 'model'))
       
    config = dict(
        # I/O data
        entity_path = entity_path,
        edge_paths = edge_paths,
        checkpoint_path = checkpoint_path,
        # Graph structure
        entities= {"all": {"num_partitions": 1 }}  ,
        relations=[  # relation template setting
        {
            "name": "all_edges",
            "lhs": "all",
            "rhs": "all",
            "operator": kwargs['operator'],
        }
        ],
        dynamic_relations=kwargs['dynamic_relaitons'],
        # Scoring model
        dimension=kwargs['dimension_num'],
        global_emb=kwargs['global_emb'],
        comparator=kwargs['comparator'],
        # Training
        init_scale = kwargs['init_scale'],
        bias=kwargs['bias'],
        num_epochs=kwargs['num_epochs'],
        loss_fn=kwargs['loss_fn'],
        lr=kwargs['learning_rate'],
        # Evaluation during training
        eval_fraction=kwargs['eval_fraction'],  # to reproduce results, we need to use all training data 
    )

    return config

def parser():
    return {
        'help': 'graph embedding functionality',
        'description': 'Generate graph embedding in kgtk tsv format, here we use PytorchBigGraph as \
        low-level implementation '
    }

def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    ### IO 
    parser.add_input_file()
    parser.add_output_file()

    parser.add_argument(     '-l',"--log", dest="log_file_path",
                              help="Setting the log path [Default: None]",
                              type=Path,default=None, metavar="")
    parser.add_argument(     '-T','--temporary_directory', dest='temporary_directory',
                             help="Sepecify the directory location to store temporary file",
                             type=Path,default=Path('/tmp/'), metavar='')
    parser.add_argument(     '-ot','--output_format', dest='output_format',
                             help="Outputformat for embeddings [Default: w2v] Choice: kgtk | w2v | glove",
                             default='w2v', metavar='')
    parser.add_argument(     '-r','--retain_temporary_data', dest='retain_temporary_data',
                            help="When opearte graph, some tempory files will be generated, set True to retain these files ",
                            type=bool,default=True, metavar='True|False')
    ### Training parameters
    parser.add_argument(     '-d',"--dimension", dest="dimension_num",
                              help="Dimension of the real space the embedding live in [Default: 100]",
                              type=int,default=100, metavar="")
    parser.add_argument(     '-s',"--init_scale", dest="init_scale",
                              help="Generating the initial embedding with this standard deviation [Default: 0.001]" +
                              "If no initial embeddings are provided, they are generated by sampling each dimension" +
                              "from a centered normal distribution having this standard deviation.",
                              type=float,default=0.001, metavar="")
    parser.add_argument(     '-c','--comparator', dest='comparator',
                             help="How the embeddings of the two sides of an edge (after having already "+
                             "undergone some processing) are compared to each other to produce a score[Default: dot]," +
                             "Choice: dot|cos|l2|squared_l2",
                             default='dot',choices=['dot','cos','l2','squared_l2'],metavar='dot|cos|l2|squared_l2')
    parser.add_argument(     '-op','--operator', dest='operator',
                             help="The transformation to apply to the embedding of one of the sides of the edge " +
                             "(typically the right-hand one) before comparing it with the other one. It reflects which model that embedding uses. " +
                             "[Default:ComplEx]",
                              #default will be setting to complex_diagonal later
                             default='ComplEx',metavar='RESCAL|DistMult|ComplEx|TransE')
    parser.add_argument(     '-e','--num_epochs', dest='num_epochs',
                             help="The number of times the training loop iterates over all the edges.[Default:100]",
                             type=int,default=100, metavar='')    
    parser.add_argument(      '-b','--bias', dest='bias',
                             help="Whether use the bias choice [Default: False],If enabled, withhold the first "+
                             "dimension of the embeddings from the comparator and instead use it as a bias, adding "+
                             "back to the score. Makes sense for logistic and softmax loss functions. ",
                             type=bool,default=False, metavar='True|False')
    parser.add_argument(     '-w','--workers', dest='workers',
                             help="The number of worker processes for training. If not given, set to CPU count.",
                             type=int,default=None, metavar='')
    parser.add_argument(     '-bs','--batch_size', dest='batch_size',
                             help="The number of edges per batch.[Default:1000]",
                             type=int,default=1000, metavar='')
    parser.add_argument(     '-lf','--loss_fn', dest='loss_fn',
                             help="How the scores of positive edges and their corresponding negatives "+
                             "are evaluated.[Default: ranking], Choice: ranking|logistic|softmax",
                             # default will be setting to ranking later
                             default=None,choices=['ranking','logistic','softmax',None],metavar='ranking|logistic|softmax')
    parser.add_argument(     '-lr','--learning_rate', dest='learning_rate',
                             help="The learning rate for the optimizer.[Default: 0.1]",
                             # default will be setting to 0.1 later
                             type=float,default=None,metavar='')
    parser.add_argument(     '-ef','--eval_fraction', dest='eval_fraction',
                             help="The fraction of edges withheld from training and used to track evaluation "+
                            "metrics during training. [Defalut:0.0 training all edges ]",
                             type=float,default=0.0,metavar='')
    parser.add_argument(     '-dr','--dynamic_relaitons', dest='dynamic_relaitons',
                             help="Whether use dynamic relations (when graphs with a "+ 
	                         "large number of relations) [Default: True]",
                             type=bool, default=True, metavar='True|False')             
    parser.add_argument(     '-ge','--global_emb', dest='global_emb',
                             help="Whether use global embedding, if enabled, add to each embedding a vector that is common "
                             "to all the entities of a certain type. This vector is learned during training.[Default: False] ",
                             type=bool,default=False, metavar='True|False')
    ### kgtk format
    parser.add_argument(      "--no-output-header", dest="output_no_header", metavar="True|False",
                              help="When true, do not write a header to the output file (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)
    
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=True)
    KgtkValueOptions.add_arguments(parser)


def config_preprocess(raw_config):
    ## Setting learning rate and loss function for different algo if user doesn't assign them
    '''
    loss_fn: ranking
    learning_rate: 0.01
    operator:complex_diagonal
    '''

    algorithm_operator = {"complex":"complex_diagonal", 
                          "distmult": "diagonal", 
                          "rescal":"linear",
                          "transe":"translation"}
    try:
        algorithm = algorithm_operator[raw_config['relations'][0]['operator'].lower()]
        raw_config['relations'][0]['operator'] = algorithm
    except:
        print('Plase use valid operator! choices: RESCAL|DistMult|ComplEx|TransE', file=sys.stderr, flush=True)
        import sys
        sys.exit()

    loss_fn = raw_config['loss_fn']
    learning_rate = raw_config['lr']
    if algorithm and loss_fn and learning_rate:
        return 
    
    if  not algorithm:  # use doesn't enter anything
        raw_config['relations'][0]['operator'] = 'complex_diagonal'
        if not loss_fn:
            raw_config['loss_fn'] = 'logistic'
        if not learning_rate:
            raw_config['lr'] = 0.1
    if algorithm: # give the algorithm 
        if algorithm == 'complex_diagonal': # ComplEx
            if not loss_fn:
                raw_config['loss_fn'] = 'logistic'
            if not learning_rate:
                raw_config['lr'] = 0.1
        elif algorithm == 'translation': # TransE
            if not loss_fn:
                raw_config['loss_fn'] = 'logistic'
            if not learning_rate:
                raw_config['lr'] = 0.1
        elif algorithm == 'diagonal': # DistMult
            if not loss_fn:
                raw_config['loss_fn'] = 'ranking'
            if not learning_rate:
                raw_config['lr'] = 0.01
        else: # RESCAL
            if not loss_fn:
                raw_config['loss_fn'] = 'ranking'
            if not learning_rate:
                raw_config['lr'] = 0.01

    processed_config = raw_config
    return processed_config

# convert wv format to kgtk format ..
def generate_kgtk_output(entities_output,output_kgtk_file,output_no_header,verbose,very_verbose):

    # Open the output file.
    kw: KgtkWriter = KgtkWriter.open(#kr.column_names,
                                    ['node1', 'label', 'node2'],
                                    output_kgtk_file,
                                    #mode=KgtkWriter.Mode[kr.mode.name],
                                    mode = KgtkWriter.Mode.AUTO,
                                    require_all_columns=False,
                                    prohibit_extra_columns=False,
                                    fill_missing_columns=False,
                                    gzip_in_parallel=False,
                                    no_header=output_no_header,
                                    verbose=verbose,
                                    very_verbose=very_verbose)

    input_line_count: int = 0
    if verbose:
        logging.info("Processing the input records.", file=self.error_file, flush=True)

    MODULE_NAME = 'graph_embeddings' # __name__.split('.')[-1] 
    with open(entities_output) as wv_file:
        for line in wv_file:
            line = line.replace('\n','')   #remove  \n
            entity_name = line.split('\t')[0]
            entity_vev = ','.join(line.split('\t')[1:])
            input_line_count += 1
            kw.write([entity_name,MODULE_NAME,entity_vev]) 
             
    if verbose:
        logging.info("Processed %d records." % (input_line_count), file=self.error_file, flush=True)

    kw.close()

def generate_w2v_output(entities_output,output_kgtk_file,kwargs):
    fout = open(output_kgtk_file,'w')
    fin = open(entities_output)
    entity_num = len(fin.readlines())
    fin.close()
    fout.write(str(entity_num) + ' ' + str(kwargs['dimension_num']) + '\n')
    with open(entities_output) as fin:
        for line in fin:
            embedding = ' '.join(line.split('\t'))
            fout.write(embedding)
    fout.close()

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        verbose: bool = False,
        very_verbose: bool = False,
        **kwargs):
    """
    **kwargs stores all parameters providing by user
    """
    # print(kwargs)

    # import modules locally
    import sys
    import typing
    import os
    import logging
    from pathlib import Path
    import json,os,h5py,gzip,torch,shutil
    from torchbiggraph.config import parse_config
    from kgtk.exceptions import KGTKException
    # copy  missing file under kgtk/graph_embeddings
    from kgtk.templates.kgtkcopytemplate import KgtkCopyTemplate
    from kgtk.graph_embeddings.importers import TSVEdgelistReader,convert_input_data  
    from torchbiggraph.train import train
    from torchbiggraph.util import SubprocessInitializer, setup_logging
    from kgtk.graph_embeddings.export_to_tsv import make_tsv
    # from torchbiggraph.converters.export_to_tsv import make_tsv

    try:
        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
        
        # store the data into log file, then the console will not output anything
        if kwargs['log_file_path'] != None: 
            log_file_path = kwargs['log_file_path']
            logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] \
            - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    filename=str(log_file_path),
                    filemode='w')
            print(f'In Processing, Please go to {kwargs["log_file_path"]} to check details', file=sys.stderr, flush=True)

        tmp_folder = kwargs['temporary_directory']
        tmp_tsv_path:Path = tmp_folder / f'tmp_{input_kgtk_file.name}'
        # tmp_tsv_path:Path = input_kgtk_file.parent/f'tmp_{input_kgtk_file.name}'

        #  make sure the tmp folder exists, otherwise it will raise an exception
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)

        try:   #if output_kgtk_file is not empty, delete it
            output_kgtk_file.unlink() 
        except: pass # didn't find, then let it go

        # *********************************************
        # 0. PREPARE PBG TSV FILE
        # *********************************************
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)
        error_file: typing.TextIO = sys.stdout if kwargs.get("errors_to_stdout") else sys.stderr
        kct: KgtkCopyTemplate = KgtkCreateTmpTsv(
            input_file_path=input_kgtk_file,
            output_file_path=tmp_tsv_path,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        # prepare the graph file
        # create a tmp tsv file for PBG embedding
        
        logging.info('Generate the valid tsv format for embedding ...')
        kct.process()
        logging.info('Embedding file is ready...')
        
        # *********************************************
        # 1. DEFINE CONFIG  
        # *********************************************
        raw_config = get_config(**kwargs)

        ## setting corresponding learning rate and loss function for different algorthim
        processed_config = config_preprocess(raw_config)
        
        # temporry output folder 
        tmp_output_folder = Path(processed_config['entity_path'])

        # before moving, need to check whether the tmp folder is not empty in case of bug
        try: #if temporry output folder is alrady existing then delete it
            shutil.rmtree(tmp_output_folder)
        except: pass # didn't find, then let it go

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
        #*************************************************
        train(config, subprocess_init=subprocess_init)

        # ************************************************
        # 4. GENERATE THE OUTPUT
        # ************************************************
        # entities_output = output_kgtk_file
        entities_output = tmp_output_folder/'entities_output.tsv'
        relation_types_output = tmp_output_folder / 'relation_types_tf.tsv'

        with open(entities_output, "xt") as entities_tf, open(
            relation_types_output, "xt"
        ) as relation_types_tf:
            make_tsv(config, entities_tf, relation_types_tf)

        # output  correct format for embeddings
        if kwargs['output_format'] == 'glove': # glove format output 
            shutil.copyfile(entities_output,output_kgtk_file)
        elif kwargs['output_format'] == 'w2v': # w2v format output
            generate_w2v_output(entities_output,output_kgtk_file,kwargs)

        else: # write to the kgtk output format tsv 
            generate_kgtk_output(entities_output,
                                 output_kgtk_file,
                                 kwargs.get('output_no_header', False),
                                 verbose,
                                 very_verbose)

        logging.info(f'Embeddings has been generated in {output_kgtk_file}.')

        # ************************************************
        # 5. Garbage collection  
        # ************************************************
        if kwargs['retain_temporary_data'] == False:
            shutil.rmtree(kwargs['temporary_directory'])
            # tmp_tsv_path.unlink() # delete temporay tsv file
            # shutil.rmtree(tmp_output_folder) # deleter temporay output folder   

        if kwargs["log_file_path"] != None:
            print('Processed Finished.', file=sys.stderr, flush=True)
            logging.info(f"Process Finished.\nOutput has been saved in {repr(str(output_kgtk_file))}")
        else:
            print(f"Process Finished.\nOutput has been saved in {repr(str(output_kgtk_file))}", file=sys.stderr, flush=True)

    except Exception as e:
        raise KGTKException(str(e))
            
