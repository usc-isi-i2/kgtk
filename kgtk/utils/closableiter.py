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

    def __iter__(self)->typing.Iterator[str]:
        self.idx: int = 0
        self.lslen: int = len(self.ls)
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

    def __iter__(self)->typing.Iterator[str]:
        self.idx: int = 0
        self.lineslen: int = len(self.lines)
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

    def __iter__(self)->typing.Iterator[typing.List[str]]:
        self.idx: int = 0
        self.llslen: int = len(self.lls)
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
