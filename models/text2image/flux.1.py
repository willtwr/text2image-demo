"""Flux.1 implementation"""

# Test with https://huggingface.co/Disty0/FLUX.1-dev-qint4

from base_model import BaseT2IModel


class Flux1(BaseT2IModel):
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwds):
        return super().__call__(*args, **kwds)
