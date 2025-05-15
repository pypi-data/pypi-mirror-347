from .extractor import _X

class PDFToJSONExtractor:
    def __init__(self, prompt: str = None):
        self._impl = _X(prompt)

    def extract(self, pdf_path: str) -> dict:
        return self._impl._z(pdf_path)
