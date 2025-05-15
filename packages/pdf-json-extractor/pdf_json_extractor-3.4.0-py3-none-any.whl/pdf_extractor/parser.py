import json
import google.generativeai as genai

class PDFParser:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def parse(self, uploaded_file, prompt: str) -> dict:
        try:
            response = self.model.generate_content([uploaded_file, prompt])
            text = response.text.replace("\n", ' ').replace("```json", '').replace("```", '').strip()
            return json.loads(text)
        except Exception as e:
            raise Exception(f"Parsing failed: {e}")
