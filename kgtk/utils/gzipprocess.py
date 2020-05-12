"""
Support classes for gzip/gunzip in seperate processes.
"""

from multiprocessing import Process, Queue
import typing

from kgtk.utils.closableiter import ClosableIter

# This helper class supports running gzip in parallel.
#
# TODO: can we use attrs here?
class GzipProcess(Process):
    gzip_file: typing.TextIO

    # The line queue contains str with None as a plug.
    #
    # TODO: can we do a better job of type declaration here?
    line_queue: Queue

    GZIP_QUEUE_SIZE_DEFAULT: int = 1000

    def __init__(self,  gzip_file: typing.TextIO, line_queue: Queue):
        super().__init__()
        self.gzip_file = gzip_file
        self.line_queue = line_queue

    def run(self):
        while True:
            line: typing.Optional[str] =  self.line_queue.get()
            if line is None: # This is the plug.
                self.gzip_file.close()
                return # Exit the process.
            self.gzip_file.write(line)

    # Called from the parent process.
    def write(self, line: str):
        self.line_queue.put(line)

    # Called from the parent process.
    def close(self):
        self.line_queue.put(None) # Send the plug.
        self.join() # Wait for the plug to exit the process.

# This helper class supports running gunzip in parallel.
#
# TODO: can we use attrs here?
class GunzipProcess(Process, ClosableIter[str]):
    gzip_file: typing.TextIO

    # The line queue contains str with None as a plug.
    #
    # TODO: can we do a better job of type declaration here?
    line_queue: Queue

    GZIP_QUEUE_SIZE_DEFAULT: int = 1000

    def __init__(self,  gzip_file: typing.TextIO, line_queue: Queue):
        super().__init__()
        self.gzip_file = gzip_file
        self.line_queue = line_queue

    def run(self):
        line: str
        for line in self.gzip_file:
            self.line_queue.put(line)
        self.line_queue.put(None) # Plug the queue.

    # This is an iterator object.
    def __iter__(self)-> typing.Iterator[str]:
        return self
    
    def __next__(self)->str:
        line: typing.Optional[str] = self.line_queue.get()
        if line is None: # Have we reached the plug?
            raise StopIteration
        else:
            return line

    def close(self):
        self.gzip_file.close()

