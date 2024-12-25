from .stable_diffusion import StableDiffusion
from .stable_diffusion_art import StableDiffusionArt
from .flux1 import Flux1


class T2IFactory:
    def __init__(self):
        pass

    def _models_list(self):
        return {
            'Flux.1': Flux1,
            'StableDiffusionArt': StableDiffusionArt,
            'StableDiffusion': StableDiffusion
        }

    def get_t2i_model(self, model_name: str):
        """Initialize the selected Text to Image model"""
        return self._models_list()[model_name]
    
    def get_t2i_models_list(self):
        return self._models_list()
