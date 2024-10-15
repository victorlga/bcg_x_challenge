import os

from langchain_community.document_loaders import PyMuPDFLoader

from page import Page

class Document:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.new_data = ""
        self.start = 0
        self.end = -1
    
    def set_start(self, start: int) -> None:
        self.start = start

    def set_end(self, end: int) -> None:
        self.end = end

    def load_data(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), '../raw', f'{self.file_name}.pdf')
        loader = PyMuPDFLoader(file_path)
        self.data = loader.load()
        self.end = len(self.data)

    def clean(self) -> str:
        main_data = self.data[self.start:self.end]

        for page_data in main_data:
            page = Page(self, page_data)
            page_content = page.clean()

            # Append the cleaned content to the relevant section title
            self.new_data += " " + page_content

        return self.new_data