def get_llm_provider(provider_name: str):
    """Initialize the selected Text to Image model"""
    match provider_name:
        case "flux":
            return NotImplementedError
        case _:
            raise ValueError(f"Unrecognised LLM provider: {provider_name}")