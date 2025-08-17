import tkinter as tk
from tkinter import filedialog, ttk, messagebox, StringVar, OptionMenu
import pdfplumber
from PIL import Image
import pandas as pd
import os
import json

# Función para extraer texto o tablas de un PDF
def extract_data_from_pdf(pdf_path):
    data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                if page.extract_table():
                    tables = page.extract_table()
                    for row in tables:
                        data.append(row)
                else:
                    text = page.extract_text()
                    if text:
                        lines = text.split("\n")
                        data.extend([line.split() for line in lines])
    except Exception as e:
        print(f"Error al procesar {pdf_path}: {e}")
    return data

# Identificar encabezados relevantes
def find_headers(data):
    header_keywords = [
        "Código", "Clave", "SKU", "Artículo", "Descripción", "U.M", "UM", "Cap", "PZA","Unidad", "Precio unitario", "P.U.", "Unitario","Valor Unitario"
    ]
    for i, row in enumerate(data):
        if any(any(keyword in str(cell) for keyword in header_keywords) for cell in row):
            return i, row  # Devuelve el índice y el encabezado detectado
    return -1, []

# Función para exportar a Excel
def export_to_excel(data, resources, output_path):
    df = pd.DataFrame(data, columns=[
        "Clave",
        "Descripción",
        "Unidad",
        "Jornada",
        "Rendimiento",
    ])
    df["Insumos/Recursos"] = json.dumps(resources, ensure_ascii=False)
    df.to_excel(output_path, index=False)

# Función para abrir archivos PDF
def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        return file_paths
    return []

# Interfaz Gráfica
class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Extractor y Consolidación de Datos")
        self.root.geometry("800x600")

        # Modo de procesamiento
        self.mode_var = tk.StringVar(value="auto")

        # Botones de modo
        self.auto_button = tk.Radiobutton(self.root, text="Modo Automático", variable=self.mode_var, value="auto")
        self.auto_button.pack(anchor=tk.W)

        self.manual_button = tk.Radiobutton(self.root, text="Modo Manual", variable=self.mode_var, value="manual")
        self.manual_button.pack(anchor=tk.W)

        # Botón para seleccionar PDFs
        self.select_button = tk.Button(self.root, text="Seleccionar PDFs", command=self.load_pdfs)
        self.select_button.pack(pady=10)

        # Tabla para mostrar datos
        self.tree = ttk.Treeview(self.root, columns=("Código", "Descripción", "Unidad", "Precio"), show="headings", selectmode="extended")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Botón para eliminar filas seleccionadas
        self.delete_button = tk.Button(self.root, text="Eliminar filas seleccionadas", command=self.delete_selected_rows)
        self.delete_button.pack(pady=5)

        # Botón para exportar
        self.export_button = tk.Button(self.root, text="Exportar a Excel", command=self.export_data)
        self.export_button.pack(pady=10)

        self.data = []

    def load_pdfs(self):
        pdf_paths = select_files()
        if not pdf_paths:
            return

        auto_mode = self.mode_var.get() == "auto"
        if auto_mode:
            self.data = []
            for pdf_path in pdf_paths:
                raw_data = extract_data_from_pdf(pdf_path)
                header_row, headers = find_headers(raw_data)
                self.data.extend(self.filter_data_auto(raw_data, header_row))
        else:
            self.load_manual_mode(pdf_paths)

        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar datos en la tabla
        for row in self.data:
            self.tree.insert("", tk.END, values=row)

        messagebox.showinfo("Éxito", "PDFs procesados correctamente")

    def filter_data_auto(self, data, header_row):
        if header_row == -1:
            return []

        headers = data[header_row]
        relevant_columns = {
            "Código": ["Código", "Clave", "SKU", "Artículo"],
            "Descripción": ["Descripción", "Nombre del producto"],
            "Unidad": ["U.M", "UM", "Unidad"],
            "Precio": ["Precio unitario", "P.U.", "Valor Unitario"]
        }

        column_indices = {key: -1 for key in relevant_columns.keys()}
        for idx, header in enumerate(headers):
            for key, keywords in relevant_columns.items():
                if any(keyword in str(header) for keyword in keywords):
                    column_indices[key] = idx

        filtered_data = []
        for row in data[header_row + 1:]:
            if len(row) < len(headers):
                print(f"Fila incompleta encontrada: {row}")
                row += [""] * (len(headers) - len(row))
            try:
                filtered_row = [
                    row[column_indices["Código"]] if column_indices["Código"] != -1 else "",
                    row[column_indices["Descripción"]] if column_indices["Descripción"] != -1 else "",
                    row[column_indices["Unidad"]] if column_indices["Unidad"] != -1 else "",
                    row[column_indices["Precio"]] if column_indices["Precio"] != -1 else ""
                ]
                filtered_data.append(filtered_row)
            except IndexError as e:
                print(f"Error al procesar la fila: {row} - {e}")

        return filtered_data

    def load_manual_mode(self, pdf_paths):
        pdf_path = pdf_paths[0]
        raw_data = extract_data_from_pdf(pdf_path)
        header_row, headers = find_headers(raw_data)

        manual_window = tk.Toplevel(self.root)
        manual_window.title("Mapear Columnas")

        # Crear un marco para organizar las etiquetas y los menús
        frame = tk.Frame(manual_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        mapping_vars = []
        options = ["Código", "Descripción", "Unidad", "Precio", "Ignorar"]

        for idx, header in enumerate(headers):
            row_frame = tk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=5)

            label = tk.Label(row_frame, text=f"Columna {idx + 1}: {header}", anchor="w")
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            var = StringVar(value="Ignorar")
            dropdown = OptionMenu(row_frame, var, *options)
            dropdown.pack(side=tk.RIGHT, padx=10)
            mapping_vars.append((idx, var))

        def confirm_mapping():
            column_mapping = {key: -1 for key in ["Código", "Descripción", "Unidad", "Precio"]}
            for idx, var in mapping_vars:
                if var.get() != "Ignorar":
                    column_mapping[var.get()] = idx

            self.data = []
            for row in raw_data[header_row + 1:]:
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                mapped_row = [
                    row[column_mapping["Código"]] if column_mapping["Código"] != -1 else "",
                    row[column_mapping["Descripción"]] if column_mapping["Descripción"] != -1 else "",
                    row[column_mapping["Unidad"]] if column_mapping["Unidad"] != -1 else "",
                    row[column_mapping["Precio"]] if column_mapping["Precio"] != -1 else ""
                ]
                self.data.append(mapped_row)

            # Actualizar tabla
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in self.data:
                self.tree.insert("", tk.END, values=row)

            manual_window.destroy()

        confirm_button = tk.Button(manual_window, text="Confirmar", command=confirm_mapping)
        confirm_button.pack(pady=10)

    def delete_selected_rows(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)

    def export_data(self):
        if not self.data:
            messagebox.showerror("Error", "No hay datos para exportar")
            return

        # Actualizar self.data con los datos actuales de la tabla
        self.data = [self.tree.item(row)['values'] for row in self.tree.get_children()]

        # Adaptar los datos al nuevo formato esperado y crear lista de recursos vacía
        processed_data = [row[:3] + ["", ""] for row in self.data]
        resources = []

        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if output_path:
            export_to_excel(processed_data, resources, output_path)
            messagebox.showinfo("Éxito", f"Datos exportados a {output_path}")
          
# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()



