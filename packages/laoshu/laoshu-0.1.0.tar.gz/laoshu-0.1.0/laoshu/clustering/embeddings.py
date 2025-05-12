from __future__ import annotations
from abc import ABC, abstractmethod
from openai import OpenAI
from typing import List
import os
import asyncio


class Embeddings(ABC):
    @abstractmethod
    async def embed(self, text: List[str]) -> List[List[float]]:
        pass

    @staticmethod
    def get_embeddings() -> Embeddings:
        return OpenAIEmbeddings()


class OpenAIEmbeddings(Embeddings):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        self.openai = OpenAI(api_key=api_key)

    async def embed(self, text: List[str]) -> List[List[float]]:
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(
            None,
            lambda: self.openai.embeddings.create(
                model="text-embedding-3-small", input=text
            ),
        )
        return list(map(lambda embedding: embedding.embedding, res.data))
