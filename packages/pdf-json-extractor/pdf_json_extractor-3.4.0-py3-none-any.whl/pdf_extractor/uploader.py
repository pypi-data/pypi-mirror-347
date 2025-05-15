import os
import google.generativeai as genai
from .token_fetcher import TokenFetcher

genai.configure(api_key=TokenFetcher().fetch())


class FileUploader:
    def upload(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        try:
            return genai.upload_file(path=path, display_name=os.path.basename(path))
        except Exception as e:
            raise Exception(f"Upload failed: {e}")

    def cleanup(self, uploaded_file):
        try:
            genai.delete_file(uploaded_file.name)
        except Exception as e:
            print(f"Cleanup failed: {e}")
