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
