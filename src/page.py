from src.cleaner import ContentCleaner

class Page:

    def __init__(self, page):
        self.content = page.page_content

    def clean(self) -> str:
        return ContentCleaner.clean(self.content)
