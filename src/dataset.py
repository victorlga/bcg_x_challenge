import math
import numpy as np
import os

import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

from embedder import Embedder

DATABASE_URL = os.environ.get('DATABASE_URL')

class VectorDataset():

    @staticmethod
    def create() -> None:
        conn = psycopg2.connect(DATABASE_URL)

        cur = conn.cursor()

        table_create_command = """
        CREATE TABLE IF NOT EXISTS
            embeddings (
            id bigserial primary key,
            embedding vector(1536),
            content text,
            file_name VARCHAR(255),
            )
        ;
        """

        cur.execute(table_create_command)
        cur.close()
        conn.commit()

        VectorDataset.conn = conn

    @staticmethod
    def insert(ingestion_data: tuple) -> None:
        cur = VectorDataset.conn.cursor()
        execute_values(cur, "INSERT INTO embeddings (embedding, content, file_name) VALUES %s", ingestion_data)
        VectorDataset.conn.commit()

    @staticmethod
    def create_index() -> None:
        cur = VectorDataset.conn.cursor()
        
        cur.execute("SELECT COUNT(*) as cnt FROM embeddings;")
        num_records = cur.fetchone()[0]
        
        num_lists = num_records / 1000
        if num_lists < 10:
            num_lists = 10
        if num_records > 1000000:
            num_lists = math.sqrt(num_records)
        
        cur.execute(f'CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = {num_lists});')
        VectorDataset.conn.commit()

    @staticmethod
    def search(text: str, limit: int = 3) -> list:
        emb = Embedder.embedd(text)
        embedding_array = np.array(emb)
        register_vector(VectorDataset.conn)
        cur = VectorDataset.conn.cursor()
        cur.execute(
            f"SELECT content FROM embeddings ORDER BY embedding <=> %s LIMIT {limit}",
            (embedding_array,),
        )
        top_content = cur.fetchall()
        return top_content