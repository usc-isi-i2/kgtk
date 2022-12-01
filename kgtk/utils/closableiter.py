import abc
import typing

T = typing.TypeVar('T')

class ClosableIter(typing.Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __iter__(self)->typing.Iterator[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self)->T:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError


class ClosableIterTextIOWrapper(ClosableIter[str]):
    def __init__(self, s: typing.TextIO):
        super().__init__()
        self.s = s

    def __iter__(self)->typing.Iterator[str]:
        return self

    def __next__(self)->str:
        return self.s.__next__()

    def close(self):
        self.s.close()

class ClosableIterListStr(ClosableIter[str]):
    def __init__(self, ls: typing.List[str]):
        super().__init__()
        self.ls: typing.List[str] = ls
        self.idx: int = 0
        self.lslen: int = len(self.ls)

    def __iter__(self)->typing.Iterator[str]:
        return self

    def __next__(self)->str:
        if self.idx < self.lslen:
            result: str = self.ls[self.idx]
            self.idx += 1
            return result
        else:
            raise StopIteration

    def close(self):
        pass

class ClosableIterTextStr(ClosableIter[str]):
    def __init__(self, text: str):
        super().__init__()
        self.lines: typing.List[str] = text.split('\n')
        self.idx: int = 0
        self.lineslen: int = len(self.lines)

    def __iter__(self)->typing.Iterator[str]:
        return self

    def __next__(self)->str:
        if self.idx < self.lineslen:
            result: str = self.lines[self.idx]
            self.idx += 1
            return result
        else:
            raise StopIteration

    def close(self):
        pass

class ClosableIterListListStr(ClosableIter[typing.List[str]]):
    def __init__(self, lls: typing.List[typing.List[str]]):
        super().__init__()
        self.lls: typing.List[typing.List[str]] = lls
        self.idx: int = 0
        self.llslen: int = len(self.lls)

    def __iter__(self)->typing.Iterator[typing.List[str]]:
        return self

    def __next__(self)->typing.List[str]:
        if self.idx < self.llslen:
            result: typing.List[str] = self.lls[self.idx]
            self.idx += 1
            return result
        else:
            raise StopIteration

    def close(self):
        pass

class ClosableIterDataFrame(ClosableIter[str]):
    # Iterate over a DataFrame.
    #
    # TODO: There may be a higher-performance way to do this.
    #
    # TODO: Do we need to perform any other transformations?
    import pandas
    def __init__(self, df: pandas.DataFrame, column_separator: str):
        super().__init__()

        # Convert the DataFrame contents to a list of lists.
        # This outght to be efficient, except that all the data is copied,
        # which may consume a lot of memory.
        #
        # TODO: Provide an alternative implementation that converts
        # DataFrame rows as needed.
        self.contents = df.values.tolist() #

        self.column_names = df.columns
        self.column_separator: str = column_separator
        self.quoted_column_separator: str = '\\' + column_separator
        self.idx: int = -1
        self.lineslen: int = len(self.contents)

    def __iter__(self)->typing.Iterator[str]:
        return self

    def __next__(self)->str:
        if self.idx < self.lineslen:
            # TODO: row needs a type.
            if self.idx < 0:
                row = self.column_names
            else:
                row = self.contents[self.idx]
            self.idx += 1

            results: typing.List[str] = []
            for item in row:
                # The str(item) converts ints and floats to strings for KGTK.
                # The replace calls attempt to deal with embedded column separators.
                #
                # TODO: How should we treat lists?
                results.append(str(item).replace('\\', '\\\\').replace(self.column_separator, self.quoted_column_separator))
            
            return self.column_separator.join(results)
        else:
            raise StopIteration

    def close(self):
        # Ensure that future next() calls raise StopIteration:
        self.idx = self.lineslen

        # Release a potentially large amount of memory:
        self.contents = None
