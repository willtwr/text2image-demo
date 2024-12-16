import streamlit as st
import torch
from diffusers import FluxPipeline


# Initialize Flux.1[dev]
@st.cache_resource(max_entries=1)
def get_pipeline():
    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
    return pipe


# Construct stable diffusion pipeline
pipe = get_pipeline()

# Set Title
st.title("Stable Diffusion Demo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initiate text input disable
if "disabled" not in st.session_state:
    st.session_state.disabled = False


# Clear chat history
def delete_chat_history():
    st.session_state.messages = []


# Disable text input
def disable():
    st.session_state.disabled = True


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
if prompt := st.chat_input("User prompt here", disabled=st.session_state.disabled, on_submit=disable):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content":prompt})

    image = pipe(
        prompt,
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]

    with st.chat_message("assistant"):
        response = st.image(image)

    st.session_state.messages.append({"role": "assistant", "content": image})
    st.session_state.disabled = False
    st.rerun()
