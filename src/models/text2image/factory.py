from .stable_diffusion import StableDiffusion
from .stable_diffusion_art import StableDiffusionArt


def get_t2i_model(model_name: str):
    """Initialize the selected Text to Image model"""
    match model_name:
        case "sd":
            return StableDiffusion
        case "sdart":
            return StableDiffusionArt
        case _:
            raise ValueError(f"Unrecognised LLM provider: {model_name}")
