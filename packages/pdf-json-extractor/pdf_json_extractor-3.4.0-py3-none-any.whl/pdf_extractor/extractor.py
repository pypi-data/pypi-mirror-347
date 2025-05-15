from .uploader import FileUploader
from .parser import PDFParser
from ._prompt import DEFAULT_PROMPT

class PDFToJSONExtractor:
    def __init__(self, prompt: str = DEFAULT_PROMPT):
        self.prompt = prompt
        self.uploader = FileUploader()
        self.parser = PDFParser()

    def extract(self, pdf_path: str) -> dict:
        uploaded_file = self.uploader.upload(pdf_path)
        try:
            return self.parser.parse(uploaded_file, self.prompt)
        finally:
            self.uploader.cleanup(uploaded_file)
