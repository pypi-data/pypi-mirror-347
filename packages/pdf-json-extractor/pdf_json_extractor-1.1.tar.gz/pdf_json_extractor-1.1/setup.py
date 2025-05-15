from setuptools import setup, find_packages

setup(
    name="pdf_json_extractor",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "requests",
        "beautifulsoup4"
    ],
    description="PDF to JSON extractor",
    author="Ramesh Lanke",
    author_email="rameshlanke31@gmail.com"
)
