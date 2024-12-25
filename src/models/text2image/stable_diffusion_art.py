"""Stable Diffusion 3.5 Medium Turbo from TensorArt"""
from .base_model import BaseT2IModel
import torch
from diffusers import StableDiffusion3Pipeline


class StableDiffusionArt(BaseT2IModel):
    def __init__(self):
        self._init_model()
        
    def _init_model(self):
        """Initialize model"""
        model_id = "tensorart/stable-diffusion-3.5-medium-turbo"
        dtype = torch.float16
        pipe = StableDiffusion3Pipeline.from_pretrained(
            model_id,
            torch_dtype=dtype
        )
        pipe = pipe.to("cuda")
        self.pipe = pipe

    def __call__(self, prompt):
        image = self.pipe(
            prompt,
            num_inference_steps=8,
            guidance_scale=1.5,
            height=768,
            width=768 
        ).images[0]
        return image
