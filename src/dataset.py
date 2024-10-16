import math
import os
from textwrap import dedent
import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from src.embedder import Embedder

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

class VectorDataset:
    
    # Class attribute for database connection
    conn = None

    @staticmethod
    def create() -> None:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create the embeddings table
        table_create_command = dedent("""
            DROP TABLE IF EXISTS embeddings;

            CREATE TABLE IF NOT EXISTS
                embeddings (
                id bigserial primary key,
                embedding vector(1536),
                content text,
                file_name VARCHAR(255)
            );
        """)
        cur.execute(table_create_command)
        cur.close()
        conn.commit()

        # Store the connection in the class attribute
        VectorDataset.conn = conn

    @staticmethod
    def insert(ingestion_data: list) -> None:
        # Insert a batch of embeddings into the database
        cur = VectorDataset.conn.cursor()
        execute_values(cur, "INSERT INTO embeddings (embedding, content, file_name) VALUES %s", ingestion_data)
        VectorDataset.conn.commit()

    @staticmethod
    def create_index() -> None:
        cur = VectorDataset.conn.cursor()

        # Check the number of records to determine the number of lists for the ivfflat index
        cur.execute("SELECT COUNT(*) as cnt FROM embeddings;")
        num_records = cur.fetchone()[0]

        num_lists = num_records / 1000
        if num_lists < 10:
            num_lists = 10
        if num_records > 1_000_000:
            num_lists = math.sqrt(num_records)

        # Create the ivfflat index on the embedding vector
        cur.execute(f'CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = {num_lists});')
        VectorDataset.conn.commit()

    @staticmethod
    def search(text: str, limit: int = 3) -> list:
        # Get the embedding for the search text
        emb = Embedder.embedd(text)

        # Register the vector extension for pgvector with psycopg2
        register_vector(VectorDataset.conn)

        cur = VectorDataset.conn.cursor()

        # Search the embeddings table for the closest vectors using the cosine distance operator
        cur.execute(
            f"SELECT content FROM embeddings ORDER BY embedding <=> %s LIMIT {limit}",
            (emb,),
        )
        
        # Fetch the top matching content
        top_content = cur.fetchall()

        return top_content
