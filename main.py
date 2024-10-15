from src.dataset import VectorDataset
from src.document import Document
from src.embedder import DocEmbedder

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
    print('Criou a table\n')

    for name, start, end in zip(file_names, file_starts, file_ends):

        doc = Document(name)
        doc.load_data()
        doc.set_start(start)
        doc.set_end(end)
        curated_data = doc.clean()
        print(f'Limpou os dados para {name}')

        embedder = DocEmbedder(curated_data)
        print(f'DocEmbedder para {name}')
        ingestion_data = embedder.get()
        print(f'embedder.get para {name}')
        ingestion_data = [t + (name,) for t in ingestion_data]
        print(f'Embeddou os dados para {name}')

        VectorDataset.insert(ingestion_data)
        print(f'Inseriu para {name}')

    VectorDataset.create_index()
    print('Criou os indices\n')

    user_input = input("Text to search: ")
    contents = VectorDataset.search(user_input)

    for c in contents:
        print(f'\nConteudo: {c} \n')

if __name__ == "__main__":
    main()