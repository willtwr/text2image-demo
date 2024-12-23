"""Base class for text to image model"""

from abc import abstractmethod


class BaseT2IModel:
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @abstractmethod
    def __call__(self, *args, **kwds):
        raise NotImplementedError
