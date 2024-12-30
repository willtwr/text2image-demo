"""Image Fill (Inpainting) factory"""
from .flux1fill import Flux1Fill
from .sd2inpaint import SD2Inpaint


imagefill_models = {
    'Flux.1 Fill': Flux1Fill,
    'Stable Diffusion 2 Inpaint': SD2Inpaint
}


def get_imagefill_model(model_name: str):
    return imagefill_models[model_name]


def get_imagefill_models_list():
    return imagefill_models.keys()
