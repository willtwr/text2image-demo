"""Base class for text to image model"""

from abc import ABC, abstractmethod


class BaseT2IModel(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @abstractmethod
    def __call__(self, *args, **kwds):
        raise NotImplementedError
