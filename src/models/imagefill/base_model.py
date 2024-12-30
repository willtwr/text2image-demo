"""Abstract class for image fill (inpainting) model"""

from abc import ABC, abstractmethod


class BaseIFModel(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError
    
    @abstractmethod
    def __call__(self, *args, **kwds):
        raise NotImplementedError
