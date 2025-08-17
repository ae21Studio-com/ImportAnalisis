import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd


class TableManager:
    def __init__(self, root):
        self.root = root
        self.current_file = None

        container = ttk.Frame(root)
        container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        table_frame = ttk.Frame(container)
        table_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=(
                "Clave",
                "Descripción",
                "Unidad",
                "Jornada",
                "Rendimiento",
                "Insumos/Recursos",
            ),
            show="headings",
            selectmode="extended",
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set,
        )
        for col in (
            "Clave",
            "Descripción",
            "Unidad",
            "Jornada",
            "Rendimiento",
            "Insumos/Recursos",
        ):
            self.tree.heading(col, text=col)

        self.tree.column("Clave", width=80)
        self.tree.column("Descripción", width=250)
        self.tree.column("Unidad", width=80)
        self.tree.column("Jornada", width=80)
        self.tree.column("Rendimiento", width=100)
        self.tree.column("Insumos/Recursos", width=200)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.v_scroll.config(command=self.tree.yview)
        self.h_scroll.config(command=self.tree.xview)

        self.tree.bind("<Double-1>", self.edit_resource_cell)

        button_frame = ttk.Frame(container)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.clear_button = ttk.Button(button_frame, text="Limpiar Tabla", command=self.clear_table)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.load_excel_button = ttk.Button(button_frame, text="Cargar Archivo Excel", command=self.load_excel)
        self.load_excel_button.pack(side=tk.RIGHT, padx=5)

    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in data:
            resources = item[5] if len(item) > 5 else ""
            if isinstance(resources, list):
                resources = ";".join(resources)

            cleaned_item = [
                item[0] if len(item) > 0 else "",
                item[1] if len(item) > 1 else "",
                item[2] if len(item) > 2 else "",
                item[3] if len(item) > 3 else "",
                item[4] if len(item) > 4 else "",
                resources,
            ]
            self.tree.insert("", tk.END, values=cleaned_item)

    def edit_resource_cell(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)
        if column != "#6":
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return

        current_values = list(self.tree.item(row_id, "values"))
        current_value = current_values[5] if len(current_values) > 5 else ""
        new_value = simpledialog.askstring(
            "Editar recursos",
            "Ingrese recursos (JSON o separados por ';')",
            initialvalue=current_value,
        )
        if new_value is not None:
            current_values[5] = new_value
            self.tree.item(row_id, values=current_values)

    def delete_selected_rows(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def load_excel(self):
        input_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx")])
        if not input_path:
            return
        try:
            df = pd.read_excel(input_path).fillna("")
            data = df.values.tolist()
            self.update_table(data)
            self.current_file = input_path
            messagebox.showinfo("Éxito", "Archivo cargado correctamente")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {exc}")

    def export_data(self):
        data = [self.tree.item(row)["values"] for row in self.tree.get_children()]
        output_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if output_path:
            try:
                existing_data = pd.read_excel(output_path)
                expected_columns = [
                    "Clave",
                    "Descripción",
                    "Unidad",
                    "Jornada",
                    "Rendimiento",
                    "Insumos/Recursos",
                ]
                if not all(col in existing_data.columns for col in expected_columns):
                    messagebox.showerror(
                        "Error", "El archivo seleccionado no tiene los encabezados correctos."
                    )
                    return

                new_data = pd.DataFrame(data, columns=expected_columns)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                updated_data.to_excel(output_path, index=False)
                messagebox.showinfo(
                    "Éxito", f"Los datos se han agregado al archivo {output_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")

