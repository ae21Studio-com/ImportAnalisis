from tkinter import ttk, StringVar, OptionMenu, Button, Toplevel, Frame, filedialog, messagebox
from utils.pdf_parser import extract_data_from_pdf, find_headers
from utils.excel_handler import export_to_excel
from utils.excel_formatter import format_to_construcdata
from gui.table_manager import TableManager
from PIL import Image
import pytesseract
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Extractor y Consolidación de Datos")
        self.root.geometry("800x600")

        # Configuración del marco principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Variable para el modo
        self.mode_var = tk.StringVar(value="auto")

        # Controles superiores
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side="top", fill="x")

        self.auto_button = ttk.Radiobutton(top_frame, text="Modo Automático", variable=self.mode_var, value="auto")
        self.auto_button.pack(side="left", padx=5)

        self.manual_button = ttk.Radiobutton(top_frame, text="Modo Manual", variable=self.mode_var, value="manual")
        self.manual_button.pack(side="left", padx=5)

        # Configuración del TableManager (se pasa mode_var)
        self.table_manager = TableManager(main_frame, self.mode_var)

        # Botones inferiores
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

                        # Botones para cargar PDFs
        self.export_button = ttk.Button(bottom_frame, text="Exportar a Excel", command=self.export_data)
        self.export_button.pack(side="right", padx=5)

        self.format_button = ttk.Button(bottom_frame, text="Formatear Excel", command=self.format_excel)
        self.format_button.pack(side="right", padx=5)

        self.delete_button = ttk.Button(bottom_frame, text="Eliminar filas seleccionadas", command=self.table_manager.delete_selected_rows, )
        self.delete_button.pack(side="left", padx=5)

        self.select_button = ttk.Button(bottom_frame, text="Seleccionar PDFs", command=self.load_pdfs)
        self.select_button.pack(side="right", padx=5)



    def load_pdfs(self):
        pdf_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not pdf_paths:
            return

        auto_mode = self.mode_var.get() == "auto"
        if auto_mode:
            self.load_pdfs_auto(pdf_paths)
        else:
            self.load_pdfs_manual(pdf_paths)

    def load_pdfs_auto(self, pdf_paths):
        data = []
        for pdf_path in pdf_paths:
            raw_data = extract_data_from_pdf(pdf_path)
            header_row, headers = find_headers(raw_data)
            data.extend(self.filter_data_auto(raw_data, header_row, headers))

        self.table_manager.update_table(data)
        messagebox.showinfo("Éxito", "PDFs procesados correctamente en modo automático")

    def load_pdfs_manual(self, pdf_paths):
        pdf_path = pdf_paths[0]
        raw_data = extract_data_from_pdf(pdf_path)
        header_row, headers = find_headers(raw_data)

        manual_window = Toplevel(self.root)
        manual_window.title("Mapear Columnas")

        # Crear un marco para organizar las etiquetas y los menús
        frame = ttk.Frame(manual_window)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        mapping_vars = []
        options = ["Código", "Descripción", "Unidad", "Precio", "Ignorar"]

        for idx, header in enumerate(headers):
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", pady=5)

            label = ttk.Label(row_frame, text=f"Columna {idx + 1}: {header}", anchor="w")
            label.pack(side="left", fill="x", expand=True)

            var = StringVar(value="Ignorar")
            dropdown = OptionMenu(row_frame, var, *options)
            dropdown.pack(side="right", padx=10)
            mapping_vars.append((idx, var))

        def confirm_mapping():
            column_mapping = {key: -1 for key in ["Código", "Descripción", "Unidad", "Precio"]}
            for idx, var in mapping_vars:
                if var.get() != "Ignorar":
                    column_mapping[var.get()] = idx

            data = []
            for row in raw_data[header_row + 1:]:
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                mapped_row = [
                    row[column_mapping["Código"]] if column_mapping["Código"] != -1 else "",
                    row[column_mapping["Descripción"]] if column_mapping["Descripción"] != -1 else "",
                    row[column_mapping["Unidad"]] if column_mapping["Unidad"] != -1 else "",
                    row[column_mapping["Precio"]] if column_mapping["Precio"] != -1 else ""
                ]
                data.append(mapped_row)

            self.table_manager.update_table(data)
            manual_window.destroy()

        confirm_button = Button(manual_window, text="Confirmar", command=confirm_mapping)
        confirm_button.pack(pady=10)

    def filter_data_auto(self, data, header_row, headers):
        if header_row == -1:
            return []

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
                row += [""] * (len(headers) - len(row))
            try:
                filtered_row = [
                    row[column_indices["Código"]] if column_indices["Código"] != -1 else "",
                    row[column_indices["Descripción"]] if column_indices["Descripción"] != -1 else "",
                    row[column_indices["Unidad"]] if column_indices["Unidad"] != -1 else "",
                    row[column_indices["Precio"]] if column_indices["Precio"] != -1 else ""
                ]
                filtered_data.append(filtered_row)
            except IndexError:
                pass

        return filtered_data

    def export_data(self):
        self.table_manager.export_data()

    def format_excel(self):
        input_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not input_path:
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not output_path:
            return

        try:
            format_to_construcdata(input_path, output_path)
            messagebox.showinfo("Éxito", "Archivo formateado correctamente")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo formatear el archivo: {exc}")



