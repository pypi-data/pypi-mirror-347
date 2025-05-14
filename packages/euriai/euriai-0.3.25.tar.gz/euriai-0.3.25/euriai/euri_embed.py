import requests
import numpy as np
from llama_index.core.embeddings.base import BaseEmbedding

class EuriaiLlamaIndexEmbedding(BaseEmbedding):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.euron.one/api/v1/euri/alpha/embeddings"

    def _post_embedding(self, texts):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "input": texts,
            "model": self.model
        }
        response = requests.post(self.url, headers=headers, json=payload)
        response.raise_for_status()
        return [np.array(obj["embedding"]).tolist() for obj in response.json()["data"]]

    def get_text_embedding(self, text: str) -> list[float]:
        return self._post_embedding([text])[0]

    def get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self._post_embedding(texts)