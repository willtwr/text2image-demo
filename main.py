import time
import random
import streamlit as st

import torch
from diffusers import StableDiffusion3Pipeline, BitsAndBytesConfig, SD3Transformer2DModel


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Clear chat history
def delete_chat_history():
    st.session_state.messages = []


# Initialize Stable Diffusion 3.5 (Quantized to reduce VRAM requirement)
model_id = "stabilityai/stable-diffusion-3.5-medium"
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
pipe = StableDiffusion3Pipeline.from_pretrained(
    model_id, 
    transformer=model_nf4,
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda")

# Set Title
st.title("Stable Diffusion Demo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], str):
            st.markdown(message["content"])
        else:
            st.image(message["content"])

# Clear chat history
with st.sidebar:
    if st.button("Clear"):
        delete_chat_history()
        st.rerun()

# System greeting
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        prompt = "Hi! What do you want to draw?"
        st.markdown(prompt)
        st.session_state.messages.append({"role": "assistant", "content": prompt})

# User input
if prompt := st.chat_input("User prompt here?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content":prompt})

    image = pipe(
        prompt,
        num_inference_steps=28,
        guidance_scale=3.5,
    ).images[0]

    with st.chat_message("assistant"):
        response = st.image(image)

    st.session_state.messages.append({"role": "assistant", "content": image})
