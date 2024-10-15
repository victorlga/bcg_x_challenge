class Document:

    def __init__(self, data: list, key: str):
        self.data = data
        self.new_data = ""
        self.key = key
        self.start = 0
        self.end = len(data)
    
    def set_start(self, start: int):
        self.start = start

    def set_end(self, end: int):
        self.end = end

    def clean(self) -> str:
        main_data = self.data[self.start:self.end]

        for page_data in main_data:
            page = Page(self, page_data)
            page_content = page.clean()

            # Append the cleaned content to the relevant section title
            self.new_data += " " + page_content

        return self.new_data