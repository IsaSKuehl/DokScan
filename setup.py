from setuptools import setup, find_packages

setup(
    name="dokscan",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "watchdog==3.0.0",
        "pdfplumber==0.10.3",
        "pypdf==4.0.0",
        "pytesseract==0.3.13",
        # "Pillow==11.0.0",  # Install separately on Windows with Python 3.14
        "msgraph-sdk==1.0.0",
        "azure-identity==1.15.0",
        "python-dotenv==1.0.0",
        "PyYAML==6.0.1",
        "fpdf==1.7.2",
    ],
)