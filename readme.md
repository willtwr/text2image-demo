# Text to Image Demo
This repo contains demo for generating image based on user prompt.
- Model: stable diffusion 3.5 medium
- UI: Streamlit
- Require NVIDIA GPU

## How to install
1. Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Create environment: `conda create -n sd python=3.11`
3. Activate environment: `conda activate sd`
4. Install [Pytorch](https://pytorch.org/get-started/locally/)
5. Install the required libraries: `pip install -r requirements.txt`

## Huggingface Access Token
1. Follow [this](https://huggingface.co/docs/hub/en/security-tokens) to create access token.
2. Go to [this](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium) to register to use the model.
3. In terminal, after activating `sd` environment, type `huggingface-cli login` and key in the created access token to login.

## How to run
1. Run the following command: `PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.9,max_split_size_mb:512 streamlit run main.py`
2. Open the Local URL in a browser.

## Example
![](assets/sd-example1.png)