import requests
from typing import List
from llama_index.core.llms import LLM
from llama_index.core.base.llms.types import ChatMessage, CompletionResponse, CompletionResponseGen


class EuriaiLlamaIndexLLM(LLM):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-nano",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.url = "https://api.euron.one/api/v1/chat/completions"

    @property
    def metadata(self):
        return {
            "context_window": 8000,
            "num_output": self.max_tokens,
            "is_chat_model": True,
            "model_name": self.model,
        }

    def chat(self, messages: List[ChatMessage], **kwargs) -> CompletionResponse:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

        return CompletionResponse(text=content)

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        return self.chat([ChatMessage(role="user", content=prompt)])

    # Async versions (not supported, so raise or return NotImplementedError)
    async def achat(self, messages: List[ChatMessage], **kwargs) -> CompletionResponse:
        raise NotImplementedError("Async chat not implemented for Euriai.")

    async def acomplete(self, prompt: str, **kwargs) -> CompletionResponse:
        raise NotImplementedError("Async complete not implemented for Euriai.")

    def stream_chat(self, messages: List[ChatMessage], **kwargs) -> CompletionResponseGen:
        raise NotImplementedError("Streaming not supported in EuriaiLlamaIndexLLM.")

    def stream_complete(self, prompt: str, **kwargs) -> CompletionResponseGen:
        raise NotImplementedError("Streaming not supported in EuriaiLlamaIndexLLM.")

    async def astream_chat(self, messages: List[ChatMessage], **kwargs) -> CompletionResponseGen:
        raise NotImplementedError("Async streaming not supported in EuriaiLlamaIndexLLM.")

    async def astream_complete(self, prompt: str, **kwargs) -> CompletionResponseGen:
        raise NotImplementedError("Async streaming not supported in EuriaiLlamaIndexLLM.")
