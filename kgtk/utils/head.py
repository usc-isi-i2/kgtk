from collections import deque
from pathlib import Path
import sys
import typing

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import TextIO


class Head(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 edge_limit: int = 10,
                 output_format: str = 'kgtk',
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 error_file: TextIO = sys.stderr,
                 show_options: bool = False,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.edge_limit = edge_limit
        self.output_format = output_format
        self.reader_options = reader_options
        self.value_options = value_options
        self.error_file = error_file
        self.show_options = show_options
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):
        # Show the final option structures for debugging and documentation.
        if self.show_options:
            print("--input-file=%s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
            print("--output-file=%s" % str(self.output_kgtk_file), file=self.error_file, flush=True)
            print("--edges=%s" % str(self.edge_limit), file=self.error_file, flush=True)
            self.reader_options.show(out=self.error_file)
            self.value_options.show(out=self.error_file)
            print("=======", file=self.error_file, flush=True)

        try:
            kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                             options=self.reader_options,
                                             value_options=self.value_options,
                                             error_file=self.error_file,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )

            output_mode: KgtkWriter.Mode = KgtkWriter.Mode.NONE
            if kr.is_edge_file:
                output_mode = KgtkWriter.Mode.EDGE
                if self.verbose:
                    print("Opening the output edge file: %s" % str(self.output_kgtk_file), file=self.error_file,
                          flush=True)

            elif kr.is_node_file:
                output_mode = KgtkWriter.Mode.NODE
                if self.verbose:
                    print("Opening the output node file: %s" % str(self.output_kgtk_file), file=self.error_file,
                          flush=True)

            else:
                if self.verbose:
                    print("Opening the output file: %s" % str(self.output_kgtk_file), file=self.error_file, flush=True)

            kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                             self.output_kgtk_file,
                                             use_mgzip=self.reader_options.use_mgzip,  # Hack!
                                             mgzip_threads=self.reader_options.mgzip_threads,  # Hack!
                                             gzip_in_parallel=False,
                                             mode=output_mode,
                                             output_format=self.output_format,
                                             error_file=self.error_file,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)

            edge_count: int = 0
            row: typing.List[str]
            if self.edge_limit > 0:
                for row in kr:
                    edge_count += 1
                    if edge_count > self.edge_limit:
                        break
                    kw.write(row)
            else:
                edge_buffer: deque = deque()
                for row in kr:
                    edge_buffer.append(row)
                    if len(edge_buffer) > - self.edge_limit:
                        edge_count += 1
                        kw.write(edge_buffer.popleft())

            kw.close()

            if self.verbose:
                print("Copied %d edges." % edge_count, file=self.error_file, flush=True)

        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))
