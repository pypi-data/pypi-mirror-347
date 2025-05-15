from setuptools import setup, find_packages

setup(
    name="pdf_json_extractor",         
    version="2.4.0",
    description="PDF to JSON extractor with obfuscated internals",
    author="RameshLanke",
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        "google-generativeai",
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
