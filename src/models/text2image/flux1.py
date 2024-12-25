"""Flux.1 implementation"""
from .base_model import BaseT2IModel
import torch
from diffusers import FluxPipeline, FluxTransformer2DModel, BitsAndBytesConfig
from transformers import T5EncoderModel


class Flux1(BaseT2IModel):
    def __init__(self):
        self._init_model()

    def _init_model(self):
        """Initialize model"""
        bfl_repo = "black-forest-labs/FLUX.1-schnell"
        dtype = torch.bfloat16
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=dtype
        )
        transformer = FluxTransformer2DModel.from_pretrained(
            bfl_repo, 
            subfolder="transformer", 
            quantization_config=quantization_config, 
            torch_dtype=dtype
        )
        t5_nf4 = T5EncoderModel.from_pretrained("diffusers/t5-nf4", torch_dtype=dtype)
        pipe = FluxPipeline.from_pretrained(
            bfl_repo,
            text_encoder_2=t5_nf4,
            transformer=transformer,
            torch_dtype=dtype
        )
        pipe = pipe.to("cuda")
        self.pipe = pipe

    def __call__(self, prompt):
        image = self.pipe(
            prompt,
            width=768,
            height=768,
            guidance_scale=2.0,
            num_inference_steps=4
        ).images[0]
        return image
