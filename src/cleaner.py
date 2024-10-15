import re

class ContentCleaner:

    @staticmethod
    def clean_line_numbers(content: str) -> str:
        pattern = r"\n\d+\s*\n"
        return re.sub(pattern, "", content)

    @staticmethod
    def clean_page_footer(content: str) -> str:
        pattern = r"\n\d+ \|Plano Nacional de Adaptação à Mudança do Clima \n"
        return re.sub(pattern, "", content)

    @staticmethod
    def clean_width_unicode(content: str) -> str:
        pattern = r"[\u200b]+"
        return re.sub(pattern, "", content)

    @staticmethod
    def clean_double_spaces(content: str) -> str:
        pattern = r"\s+"
        return re.sub(pattern, " ", content)

    @staticmethod
    def clean_urls(content: str) -> str:
        pattern = r"https?://[^\s]+"
        return re.sub(pattern, "", content)

    @staticmethod
    def clean(content: str) -> str:
        content = ContentCleaner.clean_width_unicode(content)
        content = ContentCleaner.clean_line_numbers(content)
        content = ContentCleaner.clean_page_footer(content)
        content = ContentCleaner.clean_double_spaces(content)
        content = ContentCleaner.clean_urls(content)
        return content