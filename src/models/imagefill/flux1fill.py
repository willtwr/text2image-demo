"""Flux.1 Fill (inpainting) dev implementation"""
from .base_model import BaseIFModel
import torch
from diffusers import FluxFillPipeline, FluxTransformer2DModel, BitsAndBytesConfig
from transformers import T5EncoderModel


class Flux1Fill(BaseIFModel):
    def __init__(self):
        self._init_model()

    def _init_model(self):
        """Initialize model"""
        bfl_repo = "black-forest-labs/FLUX.1-Fill-dev"
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
        pipe = FluxFillPipeline.from_pretrained(
            bfl_repo,
            text_encoder_2=t5_nf4,
            transformer=transformer,
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
            guidance_scale=30,
            num_inference_steps=50
        ).images[0]
        return image
