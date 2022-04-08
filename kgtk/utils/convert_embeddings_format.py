import sys
from pathlib import Path
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.exceptions import KGTKException
from typing import Tuple, Optional

from kgtk.io.kgtkwriter import KgtkWriter

WORD2VEC = 'word2vec'
GPROJECTOR = 'gprojector'


class ConvertEmbeddingsFormat(object):
    def __init__(self,
                 input_file: Path,
                 output_file: Path,
                 node_file: Path = None,
                 output_format: Optional[str] = WORD2VEC,
                 input_property: Optional[str] = 'embeddings',
                 metadata_columns: Optional[str] = None,
                 output_metadata_file: Path = None,
                 error_file: str = sys.stderr,
                 line_separator: str = ",",
                 **kwargs
                 ):
        if output_format not in (WORD2VEC, GPROJECTOR):
            raise KGTKException(f'--output-format should be one of "{WORD2VEC}" or "{GPROJECTOR}')
        self.input_file = input_file
        self.output_file = output_file
        self.node_file = node_file
        self.output_format = output_format.lower()
        self.input_property = input_property
        self.line_separator = line_separator
        if output_metadata_file is None:
            output_metadata_file = f"{str(Path.home())}/kgtk_embeddings_gprojector_metadata.tsv"
        self.output_metadata_file = output_metadata_file

        self.metadata_columns = metadata_columns.split(",") if metadata_columns is not None else []

        self.error_file = error_file

        self.reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)

    def process(self):
        kw_metadata = None
        node_metadata = {}

        row_count = 0
        if self.output_format == GPROJECTOR:
            node_metadata = self.read_node_file()
            metadata_column_names = node_metadata['column_names'] if node_metadata else self.metadata_columns
            kw_metadata = KgtkWriter.open(file_path=self.output_metadata_file,
                                          error_file=self.error_file,
                                          column_names=metadata_column_names,
                                          mode=KgtkWriter.Mode.NONE,
                                          require_all_columns=False,
                                          no_header=False)

        kw: KgtkWriter = KgtkWriter.open(file_path=self.output_file,
                                         error_file=self.error_file,
                                         column_names=[],
                                         mode=KgtkWriter.Mode.NONE,
                                         require_all_columns=False,
                                         no_header=True)

        kr: KgtkReader = KgtkReader.open(self.input_file,
                                         error_file=self.error_file,
                                         mode=KgtkReaderMode.EDGE,
                                         options=self.reader_options
                                         )
        if self.node_file is None and self.output_format == GPROJECTOR and len(self.metadata_columns) > 0:
            columns_not_found = []
            for col in self.metadata_columns:
                if col not in kr.column_name_map:
                    columns_not_found.append(col)
            if len(columns_not_found) > 0:
                kr.close()
                kw.close()
                if kw_metadata:
                    kw_metadata.close()
                raise KGTKException(
                    f"The following metadata columns are not found in the input file: {','.join(columns_not_found)}")

        if self.output_format == WORD2VEC:
            # first line is number of vectors and vector dimension
            line_count, dimension_count = self.count_lines(kr)
            kw.writeline(f"{line_count} {dimension_count}")

            kr.close()

            kr: KgtkReader = KgtkReader.open(self.input_file,
                                             error_file=self.error_file,
                                             mode=KgtkReaderMode.EDGE,
                                             options=self.reader_options
                                             )

        for row in kr:
            node1 = row[kr.node1_column_idx]
            node2 = row[kr.node2_column_idx]
            if row[kr.label_column_idx] == self.input_property:
                if self.output_format == WORD2VEC:
                    kw.writeline(f"{node1} {self.line_to_w2v(node2)}")
                elif self.output_format == GPROJECTOR:
                    if row_count == 10000:  # google projector will only handle upto 10000 rows
                        break
                    row_count += 1
                    node2_gp = self.line_to_gprojector(node2)
                    node1_metadata = ""
                    if node2_gp != "":
                        kw.writeline(node2_gp)
                        if node_metadata:
                            if node1 in node_metadata:
                                node1_metadata = "\t".join(node_metadata[node1].values())
                        elif len(self.metadata_columns) > 0:
                            values = [row[kr.column_name_map[x]] for x in self.metadata_columns]
                            node1_metadata = "\t".join(values)
                        kw_metadata.writeline(node1_metadata)

        kw.close()
        kr.close()
        if kw_metadata:
            kw_metadata.close()

    def count_lines(self, kr: KgtkReader) -> Tuple[int, int]:
        line_count = 0
        dimension_count = 0
        for row in kr:
            node2 = row[kr.node2_column_idx]
            if row[kr.label_column_idx] == self.input_property:
                if dimension_count == 0:
                    dimension_count = len(node2.split(self.line_separator))
                line_count += 1
        if line_count == 0 and dimension_count == 0:
            raise KGTKException(f"Zero rows in the input file with property: {self.input_property}")

        return line_count, dimension_count

    def line_to_w2v(self, line: str) -> str:
        if line is None or line.strip() == "":
            return ""

        return " ".join(line.strip().split(self.line_separator))

    def line_to_gprojector(self, line: str) -> str:
        if line is None or line.strip() == "":
            return ""

        return "\t".join(line.strip().split(self.line_separator))

    def read_node_file(self) -> dict:
        node_metadata = {}
        if self.node_file is None:
            return node_metadata

        kr_node: KgtkReader = KgtkReader.open(self.node_file,
                                              error_file=self.error_file,
                                              options=self.reader_options,
                                              mode=KgtkReaderMode.NONE,
                                              )
        columns_not_found = []
        if len(self.metadata_columns) > 0:
            for col in self.metadata_columns:
                if col not in kr_node.column_names:
                    columns_not_found.append(col)
            node_metadata['column_names'] = self.metadata_columns
        else:
            node_metadata['column_names'] = kr_node.column_names

        if len(columns_not_found) > 0:
            kr_node.close()
            raise KGTKException(
                f"The following metadata columns are not found in the node file: {','.join(columns_not_found)}")

        for row in kr_node:
            if len(row) == len(kr_node.column_names):
                node_id = row[kr_node.id_column_idx]
                if node_id not in node_metadata:
                    node_metadata[node_id] = dict()
                for col in node_metadata['column_names']:
                    node_metadata[node_id][col] = row[kr_node.column_name_map[col]]
        kr_node.close()
        return node_metadata
