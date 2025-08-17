import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

from gui.table_manager import TableManager
from utils.excel_formatter import format_to_construcdata


class ExcelFormatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Formateador ConstrucData")
        self.root.geometry("800x600")

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.table_manager = TableManager(main_frame)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.export_button = ttk.Button(bottom_frame, text="Exportar a Excel", command=self.export_data)
        self.export_button.pack(side="right", padx=5)

        self.format_button = ttk.Button(bottom_frame, text="Formatear Excel", command=self.format_excel)
        self.format_button.pack(side="right", padx=5)

        self.delete_button = ttk.Button(
            bottom_frame,
            text="Eliminar filas seleccionadas",
            command=self.table_manager.delete_selected_rows,
        )
        self.delete_button.pack(side="left", padx=5)

    def export_data(self):
        self.table_manager.export_data()

    def format_excel(self):
        input_path = self.table_manager.current_file
        if not input_path:
            messagebox.showwarning("Advertencia", "Primero cargue un archivo Excel.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
        )
        if not output_path:
            return

        try:
            format_to_construcdata(input_path, output_path)
            df = pd.read_excel(output_path)
            expected_headers = [
                "Clave",
                "Descripción",
                "Unidad",
                "Jornada",
                "Rendimiento",
                "Insumos/Recursos",
            ]
            if not all(header in df.columns for header in expected_headers):
                raise ValueError(
                    "El archivo formateado no contiene los encabezados esperados"
                )
            data = df[expected_headers].fillna("").values.tolist()
            self.table_manager.update_table(data)
            messagebox.showinfo("Éxito", "Archivo formateado correctamente")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo formatear el archivo: {exc}")

