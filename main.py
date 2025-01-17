import tkinter as tk
from tkinter import Tk
from gui.app import PDFExtractorApp
import subprocess
import sys
import pytesseract
import importlib
from pytesseract import get_tesseract_version

def check_and_install(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"El paquete '{package}' no está instalado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"'{package}' instalado con éxito.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar '{package}': {e}")
            sys.exit(1)

def ensure_dependencies():
    dependencies = {
        "pytesseract": "pytesseract",
        "PIL": "pillow",
        "pandas": "pandas"
    }
    for module, package in dependencies.items():
        check_and_install(package)
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract OCR encontrado: versión {version}")
    except FileNotFoundError:
        print("No se encontró Tesseract OCR. Asegúrate de que está instalado y configurado correctamente.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al verificar Tesseract: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_dependencies()
    root = Tk()
    app = PDFExtractorApp(root)
    root.mainloop()




