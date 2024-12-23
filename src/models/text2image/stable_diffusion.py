from .base_model import BaseT2IModel
import torch
from diffusers import StableDiffusion3Pipeline, BitsAndBytesConfig, SD3Transformer2DModel
from transformers import T5EncoderModel


class StableDiffusion(BaseT2IModel):
    def __init__(self):
        self._init_model()
        
    def _init_model(self):
        """Initialize model"""
        model_id = "stabilityai/stable-diffusion-3.5-large-turbo"
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model_nf4 = SD3Transformer2DModel.from_pretrained(
            model_id,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.bfloat16
        )
        t5_nf4 = T5EncoderModel.from_pretrained("diffusers/t5-nf4", torch_dtype=torch.bfloat16)
        pipe = StableDiffusion3Pipeline.from_pretrained(
            model_id, 
            transformer=model_nf4,
            text_encoder_3=t5_nf4,
            torch_dtype=torch.bfloat16
        )
        pipe = pipe.to("cuda")
        self.pipe = pipe

    def __call__(self, prompt):
        image = self.pipe(
            prompt,
            num_inference_steps=4,
            guidance_scale=0.0,
            # max_sequence_length=512,
            height=768,
            width=768 
        ).images[0]
        return image
