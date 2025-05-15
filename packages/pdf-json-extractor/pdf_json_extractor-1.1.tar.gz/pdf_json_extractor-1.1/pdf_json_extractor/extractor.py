import os
import json
import google.generativeai as genai
from ._prompt import DEFAULT_PROMPT
from .token_fetcher import fetch_token

genai.configure(api_key=fetch_token())

def extract_pdf_to_json(pdf_file_path, prompt=None):
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"PDF file not found at '{pdf_file_path}'")

    prompt = prompt or DEFAULT_PROMPT

    try:
        uploaded_file = genai.upload_file(path=pdf_file_path, display_name=os.path.basename(pdf_file_path))
    except Exception as e:
        raise Exception(f"Error uploading file: {e}")

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    try:
        response = model.generate_content([uploaded_file, prompt])
        response_text = response.text.replace("\n", ' ').replace("```json", '').replace("```", '').strip()
        json_data = json.loads(response_text)
        return json_data
    except Exception as e:
        try:
            genai.delete_file(uploaded_file.name)
        except Exception as cleanup_err:
            print(f"Cleanup failed for file {uploaded_file.name}: {cleanup_err}")
        raise Exception(f"Error generating content: {e}")
