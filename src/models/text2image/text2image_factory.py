"""Factory for Text to Image models"""
from .stable_diffusion import StableDiffusion
from .stable_diffusion_art import StableDiffusionArt
from .flux1 import Flux1


text2image_models = {
    'Flux.1': Flux1,
    'StableDiffusionArt': StableDiffusionArt,
    'StableDiffusion': StableDiffusion
}


def get_t2i_model(model_name: str):
    return text2image_models[model_name]


def get_t2i_models_list():
    return text2image_models.keys()
