import os

import numpy as np
from langchain_openai import OpenAIEmbeddings

nltk.download('punkt')

from langchain.text_splitter import RecursiveCharacterTextSplitter

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the key was retrieved successfully
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")

class Embedder:
    
    @staticmethod
    def embedd(text: str):
        embedding = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=OPENAI_API_KEY
        )
        return embedding.embed_query(text)

class DocEmbedder:

    def __init__(self, text: str):
        self.text = text
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=100
        )

    def get(self) -> list:
        embeddings_list, text_list = self.create_embeddings(self.text)
        return [(np.array(embedding), text,) for embedding, text in zip(embeddings_list, text_list)]

    def create_embeddings(self, text: str) -> list:
        embedding_chunk_list = []
        text_chunk_list = []
        text_split = self.text_splitter.split_text(text)

        for t in text_split:
            text_chunk_list.append(t)
            emb = Embedder.embedd(t)
            embedding_chunk_list.append(emb)

        return embedding_chunk_list, text_chunk_list