import sys
import torch
import typing
import logging
from typing import List
from pathlib import Path
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.exceptions import KGTKException
from sentence_transformers import SentenceTransformer
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions


class EmbeddingVector:
    def __init__(self,
                 model_name=None,
                 output_property_name: str = "text_embedding",
                 sentence_property_name: str = "sentence",
                 output_format: str = "kgtk"):
        self._logger = logging.getLogger(__name__)
        if not model_name:
            self.model_name = 'bert-base-nli-mean-tokens'
        else:
            self.model_name = model_name
        self._logger.info("Using model {}".format(self.model_name))
        if torch.cuda.is_available():
            self.model = SentenceTransformer(self.model_name, device=('cuda:0'))
        else:
            self.model = SentenceTransformer(self.model_name)

        self.selected_gpu_device_index = 0
        self.total_gpu_count = torch.cuda.device_count()
        self.column_names = ['node1', 'label', 'node2']
        self.error_file = sys.stderr
        self.output_property_name = output_property_name
        self.sentence_property_name = sentence_property_name
        self.output_format = output_format

    def retry_next_gpu(self, error):
        self.selected_gpu_device_index += 1
        if self.selected_gpu_device_index >= self.total_gpu_count:
            self._logger.error("Attempted task on all available GPUs")
            raise error
        else:
            self.model = SentenceTransformer(self.model_name, device=('cuda:' + str(self.selected_gpu_device_index)))
            self._logger.debug(f"Reattempting task on GPU device: {('cuda:' + str(self.selected_gpu_device_index))}")

    def get_sentences_embedding(self, sentences: typing.List[str]):
        """
            transform a list of sentences to embedding vectors
        """
        while True:
            # Re-attempt executing the model on a different GPU until all GPU's have been tried
            try:
                sentence_embeddings = self.model.encode(sentences, show_progress_bar=True)
                break  # If there is no error, this will break the loop and return the results
            except RuntimeError as e:
                self.retry_next_gpu(e)
        return sentence_embeddings

    def process_sentences_kgtk(self,
                               input_file_path: Path,
                               output_file_path: Path,
                               error_file: typing.TextIO = sys.stderr,
                               reader_options: typing.Optional[KgtkReaderOptions] = None,
                               value_options: typing.Optional[KgtkValueOptions] = None,
                               verbose: bool = False,
                               batch_size: int = 100000
                               ):
        kr: KgtkReader = KgtkReader.open(input_file_path,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         )
        if kr.node1_column_idx < 0:
            raise KGTKException("Missing column: node1 or alias")
        if kr.label_column_idx < 0:
            raise KGTKException("Missing column: label or alias")
        if kr.node2_column_idx < 0:
            raise KGTKException("Missing column: node2 or alias")

        self._logger.debug("node1 column index = {}".format(kr.node1_column_idx))
        self._logger.debug("label column index = {}".format(kr.label_column_idx))
        self._logger.debug("node2 column index = {}".format(kr.node2_column_idx))

        sentences = []
        qnodes = []

        all_qnodes = []
        all_vectors = []

        if self.output_format == 'kgtk':
            kw: KgtkWriter = KgtkWriter.open(self.column_names,
                                             output_file_path,
                                             require_all_columns=False,
                                             error_file=self.error_file
                                             )
        else:
            kw = open(output_file_path, 'w')

        for row in kr:
            if 0 < batch_size == len(sentences):
                vectors = self.get_sentences_embedding(sentences)
                if self.output_format == 'kgtk':
                    self.write_vectors(kw, self.output_property_name, qnodes, vectors)
                else:
                    all_qnodes.extend(qnodes)
                    all_vectors.extend(vectors)
                sentences = []
                qnodes = []
            else:
                if row[kr.label_column_idx].strip() == self.sentence_property_name:
                    qnodes.append(row[kr.node1_column_idx])
                    sentences.append(row[kr.node2_column_idx])

        if len(qnodes) > 0 and len(sentences) > 0:
            vectors = self.get_sentences_embedding(sentences)
            if self.output_format == 'kgtk':
                self.write_vectors(kw, self.output_property_name, qnodes, vectors)
            else:
                all_qnodes.extend(qnodes)
                all_vectors.extend(vectors)

        if len(all_qnodes) > 0 and len(all_vectors) > 0 and self.output_format == 'w2v':
            kw.write(f'{len(all_qnodes)} {len(all_vectors[0])}\n')
            for qnode, vector in zip(all_qnodes, all_vectors):
                kw.write(f'{qnode} {" ".join(map(str, vector))}\n')

        kr.close()
        kw.close()

    @staticmethod
    def write_vectors(kw: KgtkWriter, property_name: str, qnodes: typing.List[str], vectors: List[float]):
        for qnode, vector in zip(qnodes, vectors):
            kw.write([qnode, property_name, ",".join(map(str, vector))])
