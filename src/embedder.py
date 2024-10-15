import os

from langchain_openai import OpenAIEmbeddings
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
        return [(embedding, text,) for embedding, text in zip(embeddings_list, text_list)]

    def create_embeddings(self, text: str) -> list:
        embedding_chunk_list = []
        text_chunk_list = []
        text_split = self.text_splitter.split_text(text)

        for i, t in enumerate(text_split):
            # Build the broader context: concatenate previous, current, and next text chunks if they exist
            previous_chunk = text_split[i - 1] if i > 0 else ''
            current_chunk = t
            next_chunk = text_split[i + 1] if i < len(text_split) - 1 else ''
            
            # Concatenate for broader context
            broader_context = previous_chunk + current_chunk + next_chunk
            text_chunk_list.append(broader_context)

            # Generate embedding for the current chunk only (t)
            emb = Embedder.embedd(t)
            embedding_chunk_list.append(emb)

        return embedding_chunk_list, text_chunk_list