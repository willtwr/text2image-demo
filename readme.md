# Text to Image Demo (work in progress)
This repo contains demo for generating image based on user prompt. It runs model locally for the sake of PoC and is not suitable for production. Require NVIDIA GPU to run.

# TODO:
- [x] Implement Stable Diffusion.
- [x] Implement Flux.1.
- [x] Refactor text-to-image models to factory approach.
- [x] Add model switch.
- [ ] Explore storage in NiceGUI.
- [ ] To explore Auto1111sdk.

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
<table>
    <tr>
        <td>Stable Diffusion 3.5 Large Turbo Quantized (StabilityAI)</td>
        <td>Stable Diffusion 3.5 Medium Turbo (TensorArt)</td>
        <td>Flux.1 Schnell Quantized (Black Forest Labs)</td>
    </tr>
    <tr>
        <td><img src="./assets/sd3.5-sample1.png"></td>
        <td><img src="./assets/sd3.5art-sample1.png"></td>
        <td><img src="./assets/flux1-schnell-sample1.png"></td>
    </tf>
</table>