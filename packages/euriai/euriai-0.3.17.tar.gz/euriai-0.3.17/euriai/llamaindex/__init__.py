def __init__(
    self,
    api_key: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
):
    # Use default values directly, no `self.model` yet
    super().__init__(
        api_key=api_key,
        model=model if model is not None else "gpt-4.1-nano",
        temperature=temperature if temperature is not None else 0.7,
        max_tokens=max_tokens if max_tokens is not None else 1000,
    )
