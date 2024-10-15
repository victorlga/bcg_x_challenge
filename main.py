from dataset import VectorDataset
from document import Document
from embedder import DocEmbedder

file_names = [
    'plano-acao-adaptacao-climatica-nacional',
    'plano-acao-climatica-agro',
    'plano-acao-climatica-curitiba',
    'plano-acao-climatica-federal',
    'plano-acao-climatica-itabirito',
    'plano-acao-climatica-joao-pessoa',
    'plano-acao-climatica-sp-regiao',
    'plano-enfrentamento-mudanca-climatica-nacional',
]

file_starts = [
    5,
    20,
    15,
    8,
    15,
    13,
    6,
    0,
]

file_ends = [
    331,
    122,
    116,
    411,
    68,
    91,
    112,
    66,
]


def main():

    VectorDataset.create()

    for name, start, end in zip(file_names, file_starts, file_ends):

        doc = Document(name)
        doc.load_data()
        doc.set_start(start)
        doc.set_end(end)
        curated_data = doc.clean()

        embedder = DocEmbedder(curated_data)
        ingestion_data = embedder.get()
        ingestion_data = [t + (name,) for t in ingestion_data]

        VectorDataset.insert(ingestion_data)

    VectorDataset.create_index()

    user_input = input("Text to search: ")
    contents = VectorDataset.search(user_input)

    for c in contents:
        print(c)

if __name__ == "__main__":
    main()