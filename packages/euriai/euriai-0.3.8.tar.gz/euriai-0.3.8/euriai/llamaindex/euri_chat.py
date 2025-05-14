import requests
from llama_index.llms.base import LLM, ChatMessage, CompletionResponse
from typing import List

class EuriaiLlamaIndexLLM(LLM):
    def __init__(self, api_key: str, model: str = "gpt-4.1-nano", temperature: float = 0.7, max_tokens: int = 1000):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.url = "https://api.euron.one/api/v1/chat/completions"

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        return self.chat([ChatMessage(role="user", content=prompt)])

    def chat(self, messages: List[ChatMessage], **kwargs) -> CompletionResponse:
        payload = {
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return CompletionResponse(text=content)
