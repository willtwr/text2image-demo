"""Flux.1 implementation"""

from .base_model import BaseT2IModel
import torch
from diffusers import FluxPipeline, FluxTransformer2DModel
from transformers import T5EncoderModel, BitsAndBytesConfig


class Flux1(BaseT2IModel):
    def __init__(self):
        bfl_repo = "black-forest-labs/FLUX.1-schnell"
        dtype = torch.bfloat16
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        text_encoder_2 = T5EncoderModel.from_pretrained(
            bfl_repo, 
            subfolder="text_encoder_2", 
            quantization_config=quantization_config, 
            torch_dtype=dtype
        )
        transformer = FluxTransformer2DModel.from_pretrained(
            bfl_repo, 
            subfolder="transformer", 
            quantization_config=quantization_config, 
            torch_dtype=dtype
        )
        pipe = FluxPipeline.from_pretrained(
            bfl_repo,
            text_encoder_2=None,
            transformer=None,
            torch_dtype=torch.bfloat16
        )
        pipe.text_encoder_2 = text_encoder_2
        pipe.transformer = transformer
        pipe = pipe.to("cuda")
        self.pipe = pipe

    def __call__(self, prompt):
        image = self.pipe(
            prompt,
            width=768,
            height=768,
            guidance_scale=3.5,
            num_inference_steps=4,
            generator=torch.Generator("cpu").manual_seed(0)
        ).images[0]
        return image
