import numpy as np
import faiss
import os
from tqdm import tqdm
from kgtk.exceptions import KGTKException


# # TODO:
# - look up what is faiss.set_direct_map_type and if I need more params for this.
#   - still not sure. Very little information about it is easily available
# - add support for sharding
# - add support for cosine similarity as a distance metric


def build_faiss(embeddings_file, embeddings_format, no_input_header, index_file_out, index_to_node_file_out,
                max_train_examples, workers, index_string, metric_type, p=None, verbose=False):

    # validate input file path
    if not os.path.exists(embeddings_file):
        raise KGTKException("File path given for embeddings_file parameter does not exist: " + embeddings_file)
    if os.path.getsize(embeddings_file) == 0:
        raise KGTKException("File given for embeddings_file parameter is empty: " + embeddings_file)

    # validate metric type and translate to a faiss metric
    metrics = {
        "Inner_product": faiss.METRIC_INNER_PRODUCT,
        "L2": faiss.METRIC_L2,
        "L1": faiss.METRIC_L1,
        "Linf": faiss.METRIC_Linf,
        "Lp": faiss.METRIC_Lp,
        "Canberra": faiss.METRIC_Canberra,
        "BrayCurtis": faiss.METRIC_BrayCurtis,
        "JensenShannon": faiss.METRIC_JensenShannon
    }
    if metric_type in metrics:
        faiss_metric = metrics[metric_type]
    else:
        raise KGTKException("Unrecognized value for metric_type parameter: {}.".format(metric_type) +
                            "Please choose one of {}.".format(" | ".join(list(metrics.keys()))))
    if metric_type == "Lp" and p is None:
        raise KGTKException("When using the metric_type Lp, you must specify a value of p via " +
                            "the metric_arg parameter.")

    # validate embedding format string
    if embeddings_format not in ["w2v", "kgtk", "glove"]:
        raise KGTKException("Unrecognized value for embeddings_format parameter: {}.".format(embeddings_format) +
                            " Please choose one of kgtk | w2v | glove.")

    # file formats that have a header
    has_header = embeddings_format == "w2v" or (embeddings_format == "kgtk" and not no_input_header)

    # infer dim (TODO: possibly more validation? e.g. validate file format agrees with the given format?)
    dim = infer_embedding_dim(embeddings_file, embeddings_format, has_header)

    # Find total number of lines
    with open(embeddings_file, 'r') as f:
        num_lines = sum(1 for _ in f)

    # Build the index to node file
    if index_to_node_file_out is not None:
        if verbose:
            print("Writing index-to-node file...")
        with open(embeddings_file, 'r') as f_in:
            with open(index_to_node_file_out, 'w+') as f_out:
                f_out.write("node1\tlabel\tnode2\n")  # header
                for line_num, line in enumerate(tqdm(f_in, total=num_lines) if verbose else f_in):
                    # skip first line if there is header
                    if has_header and line_num == 0:
                        continue

                    node = line.split('\t')[0]
                    index = line_num-1 if has_header else line_num

                    f_out.write("{}\tindex_to_node\t{}\n".format(index, node))

    # TODO: support...
    # vector quantization option -- done (handled by index string / index factory)
    # sharding option

    # Load training examples for index training
    train_vecs = []
    if verbose:
        print("Loading training vectors...")
    num_lines_to_read_for_training = max_train_examples if not has_header else max_train_examples + 1
    num_lines_to_read_for_training = min(num_lines, num_lines_to_read_for_training)
    with open(embeddings_file, 'r') as f_in:
        for line_num, line in enumerate(tqdm(f_in, total=num_lines_to_read_for_training) if verbose else f_in):
            # control number of lines read
            if line_num == num_lines_to_read_for_training:
                break
            # skip header
            if has_header and line_num == 0:
                continue
            train_vecs.append(get_embedding_from_line(line, embeddings_format))
    train_vecs = np.array(train_vecs, dtype=np.float32)  # faiss requires input to be np.array of floats

    # Setting up untrained index instance...
    # Limit cpu usage
    if workers is not None:
        faiss.omp_set_num_threads(workers)
    # Instantiate index with specified metric
    index = faiss.index_factory(dim, index_string, faiss_metric)  # TODO -- add quantizer option / other options
    index.verbose = verbose
    # Set metric arguement if relevant
    if metric_type == "Lp":
        index.metric_arg = p
    # TODO -- look more into what this is doing / if need to provide more options for it.
#     index.set_direct_map_type(faiss.DirectMap.Array)

    if verbose:
        print(f"Training index using {min(num_lines,max_train_examples)} examples...")
    index.train(train_vecs)

    # Add all vecs to index
    if verbose:
        print("Adding all vectors to the trained index...")
    # Start with alread-loaded vectors used for training.
    if verbose:
        print("Adding training vectors...")
    index.add(train_vecs)
    del train_vecs  # free up space
    # Incrementally load and add any additional vectors in batches
    if num_lines_to_read_for_training < num_lines:
        if verbose:
            print("Incrementally loading and adding remaining vectors...")
        vecs = []
        batch_size = max_train_examples
        with open(embeddings_file, 'r') as f_in:
            for line_num, line in enumerate(tqdm(f_in, total=num_lines) if verbose else f_in):
                # Skip past already-added training examples
                if line_num < num_lines_to_read_for_training:
                    continue

                vecs.append(get_embedding_from_line(line, embeddings_format))

                # flush loaded vecs if we reach batch size
                if len(vecs) == batch_size:
                    index.add(np.array(vecs, dtype=np.float32))
                    vecs = []
        # add the last batch if there is anything in it
        if len(vecs) > 0:
            index.add(np.array(vecs, dtype=np.float32))

    # Save index
    faiss.write_index(index, index_file_out)


# ASSUMPTIONS:
# * embeddings_format has already been validated and is one of w2v, kgtk, or glove.
def infer_embedding_dim(embeddings_file, embeddings_format, has_header):
    with open(embeddings_file, 'r') as f:
        line = f.readline().strip()
        if embeddings_format == "w2v":
            # node count and embedding dimension are given in the first line
            dim = int(line.split("\t")[1])
        elif embeddings_format == "kgtk":
            if has_header:
                line = f.readline().strip()  # look at second line
            # comma-separated embeddings are in the 3rd column
            emb = line.split("\t")[2]
            dim = len(emb.split(","))
        else:  # embeddings_format == "glove"
            # First column is for the node, then each following column contains
            # a dimension of the corresponding embedding
            dim = len(line.split("\t")) - 1
    return dim


# ASSUMPTIONS:
# * embeddings_format has already been validated and is one of w2v, kgtk, or glove.
# * if embeddings have a header line, then the given line is not the first line from the file.
def get_embedding_from_line(line, embeddings_format):
    # formats that have embeddings in columns starting with second column
    if embeddings_format in ["w2v", "glove"]:
        emb = line.split('\t')[1:]

    # kgtk format has embeddings in 3rd column as comma delimited string
    else:
        emb = line.split('\t')[-1].split(',')

    return emb
