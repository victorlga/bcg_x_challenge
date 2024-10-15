from document import Document
from cleaner import ContentCleaner

class Page:

    def __init__(self, doc: Document, page):
        self.content = page.page_content
        self.doc = doc

    def clean(self) -> str:
        return ContentCleaner.clean(self.content)