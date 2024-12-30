"""Stable Diffusion 2 Inpainting implementation"""
from .base_model import BaseIFModel
import torch
from diffusers import StableDiffusionInpaintPipeline


class SD2Inpaint(BaseIFModel):
    def __init__(self):
        self._init_model()

    def _init_model(self):
        """Initialize model"""
        bfl_repo = "stabilityai/stable-diffusion-2-inpainting"
        dtype = torch.bfloat16
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            bfl_repo,
            torch_dtype=dtype
        )
        pipe = pipe.to("cuda")
        self.pipe = pipe

    def __call__(self, prompt, image, mask):
        image = self.pipe(
            prompt,
            image=image,
            mask_image=mask,
            width=768,
            height=768,
            guidance_scale=7.5,
            num_inference_steps=50
        ).images[0]
        return image
