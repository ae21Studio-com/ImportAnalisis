import pdfplumber

def extract_data_from_pdf(pdf_path):
    data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                if page.extract_table():
                    data.extend(page.extract_table())
                else:
                    text = page.extract_text()
                    if text:
                        data.extend([line.split() for line in text.split("\n")])
    except Exception as e:
        print(f"Error al procesar {pdf_path}: {e}")
    return data

def find_headers(data):
    header_keywords = ["Código", "Descripción", "Unidad", "Precio"]
    for i, row in enumerate(data):
        if any(keyword in str(row) for keyword in header_keywords):
            return i, row
    return -1, []
