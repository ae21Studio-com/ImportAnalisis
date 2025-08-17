import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
from utils.excel_handler import export_to_excel
import pytesseract
from PIL import Image
import cv2
import numpy as np

class TableManager:
    def __init__(self, root, mode_var):
        self.root = root  # Referencia al root
        self.mode_var = mode_var  # Variable de modo

        # Frame principal
        container = ttk.Frame(root)
        container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Frame para la tabla y los scrollbars
        table_frame = ttk.Frame(container)
        table_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Scrollbars
        self.v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        # Treeview para la tabla
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
        self.tree.heading("Clave", text="Clave")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Jornada", text="Jornada")
        self.tree.heading("Rendimiento", text="Rendimiento")
        self.tree.heading("Insumos/Recursos", text="Insumos/Recursos")

        self.tree.column("Clave", width=80)
        self.tree.column("Descripción", width=250)
        self.tree.column("Unidad", width=80)
        self.tree.column("Jornada", width=80)
        self.tree.column("Rendimiento", width=100)
        self.tree.column("Insumos/Recursos", width=200)

        # Ubicar la tabla y los scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        # Configuración de grid para expandir
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.v_scroll.config(command=self.tree.yview)
        self.h_scroll.config(command=self.tree.xview)

        # Permitir edición de recursos con doble clic
        self.tree.bind("<Double-1>", self.edit_resource_cell)

        # Frame para los botones
        button_frame = ttk.Frame(container)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Botones
        self.clear_button = ttk.Button(button_frame, text="Limpiar Tabla", command=self.clear_table)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.import_ocr_button = ttk.Button(button_frame, text="Cargar Cotización Escaneada", command=self.import_from_ocr)
        self.import_ocr_button.pack(side=tk.RIGHT, padx=5)

        # Verificar el modo inicial
        self.toggle_ocr_button()

        # Vincular la función de alternancia al cambio de modo
        self.mode_var.trace_add("write", self.toggle_ocr_button)

    def toggle_ocr_button(self, *args):
        """Alterna la visibilidad del botón OCR según el modo."""
        if self.mode_var.get() == "manual":
            self.import_ocr_button.pack(side=tk.RIGHT, padx=5)  # Mostrar el botón
        else:
            self.import_ocr_button.pack_forget()  # Ocultar el botón

    def update_table(self, data):
        """Actualiza la tabla con los datos proporcionados."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in data:
            resources = item[5] if len(item) > 5 else ""
            if isinstance(resources, list):
                resources = ";".join(resources)

            cleaned_item = [
                item[0] if len(item) > 0 else "",  # Clave
                item[1] if len(item) > 1 else "",  # Descripción
                item[2] if len(item) > 2 else "",  # Unidad
                item[3] if len(item) > 3 else "",  # Jornada
                item[4] if len(item) > 4 else "",  # Rendimiento
                resources,  # Insumos/Recursos
            ]
            self.tree.insert("", tk.END, values=cleaned_item)

    def edit_resource_cell(self, event):
        """Permite editar la columna de recursos."""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)
        if column != "#6":  # Columna Insumos/Recursos
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
        """Elimina las filas seleccionadas en la tabla."""
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)

    def clear_table(self):
        """Limpia completamente la tabla de datos."""
        for row in self.tree.get_children():
            self.tree.delete(row)

    def export_data(self):
        """Exporta los datos actuales de la tabla a Excel."""
        data = [self.tree.item(row)["values"] for row in self.tree.get_children()]
        output_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if output_path:
            try:
                # Leer el archivo existente
                existing_data = pd.read_excel(output_path)

                # Validar encabezados
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

                # Crear un DataFrame con los datos actuales
                new_data = pd.DataFrame(data, columns=expected_columns)

                # Concatenar los datos nuevos con los existentes
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)

                # Guardar el archivo actualizado
                updated_data.to_excel(output_path, index=False)
                messagebox.showinfo(
                    "Éxito", f"Los datos se han agregado al archivo {output_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")

    def import_from_ocr(self):
        """Carga y procesa una cotización escaneada usando OCR con selección manual y mapeo."""
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if not image_path:
            return

        try:
            # Permitir selección de áreas
            rects, image = self.select_areas(image_path)

            # Mostrar ventana para mapear áreas seleccionadas
            self.map_areas(rects, image)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen: {e}")

    def map_areas(self, rects, image):
        """Muestra una ventana para mapear las áreas seleccionadas a columnas."""
        if not hasattr(self, "root") or not self.root:
            raise ValueError("El objeto TableManager no tiene referencia al root de la aplicación.")

        map_window = tk.Toplevel(self.root)
        map_window.title("Mapear Áreas Seleccionadas")
        map_window.geometry("600x400")

        tk.Label(map_window, text="Mapear áreas seleccionadas a columnas").pack(pady=10)

        mapping_vars = []
        options = [
            "Clave",
            "Descripción",
            "Unidad",
            "Jornada",
            "Rendimiento",
            "Insumos/Recursos",
            "Ignorar",
        ]

        for idx, rect in enumerate(rects):
            x1, y1 = rect[0]
            x2, y2 = rect[1]
            cropped_image = image[y1:y2, x1:x2]
            preview_text = pytesseract.image_to_string(cropped_image)

            frame = tk.Frame(map_window)
            frame.pack(fill="x", pady=5)

            label = tk.Label(frame, text=f"Área {idx + 1}: {preview_text[:30]}...", anchor="w")
            label.pack(side="left", fill="x", expand=True)

            var = tk.StringVar(value="Ignorar")
            dropdown = ttk.OptionMenu(frame, var, *options)
            dropdown.pack(side="right", padx=10)
            mapping_vars.append((rect, var))

        def confirm_mapping():
            """Procesa las áreas seleccionadas y mapea los datos a las columnas correspondientes."""
            mapped_data = {
                key: []
                for key in [
                    "Clave",
                    "Descripción",
                    "Unidad",
                    "Jornada",
                    "Rendimiento",
                    "Insumos/Recursos",
                ]
            }

            # Procesar cada área seleccionada
            for rect, var in mapping_vars:
                if var.get() != "Ignorar":
                    x1, y1 = rect[0]
                    x2, y2 = rect[1]
                    cropped_image = image[y1:y2, x1:x2]
                    text = pytesseract.image_to_string(cropped_image).strip()
                    lines = text.split("\n")  # Dividir el texto en filas

                    # Limpiar y agregar los datos al mapeo correspondiente
                    cleaned_lines = [line.strip() for line in lines if line.strip()]  # Ignorar líneas vacías
                    mapped_data[var.get()].extend(cleaned_lines)

            # Asegurar que todas las columnas tengan el mismo número de filas
            max_rows = max(len(mapped_data[key]) for key in mapped_data.keys())
            for key in mapped_data.keys():
                while len(mapped_data[key]) < max_rows:
                    mapped_data[key].append("")  # Rellenar filas faltantes con ""

            # Combinar los datos de las columnas en filas completas
            data = [
                [
                    mapped_data["Clave"][i],
                    mapped_data["Descripción"][i],
                    mapped_data["Unidad"][i],
                    mapped_data["Jornada"][i],
                    mapped_data["Rendimiento"][i],
                    mapped_data["Insumos/Recursos"][i],
                ]
                for i in range(max_rows)
            ]

            # Actualizar la tabla con los datos procesados
            self.update_table(data)
            map_window.destroy()




        confirm_button = tk.Button(map_window, text="Confirmar", command=confirm_mapping)
        confirm_button.pack(pady=10)



    def select_areas(self, image_path):
        """Permite al usuario seleccionar áreas en la imagen."""
        image = cv2.imread(image_path)
        clone = image.copy()
        rects = []
        selecting = [False]  # Estado para el evento del mouse

        def click_and_crop(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                rects.append([(x, y)])  # Inicio del rectángulo
                selecting[0] = True
            elif event == cv2.EVENT_LBUTTONUP:
                rects[-1].append((x, y))  # Fin del rectángulo
                selecting[0] = False
                cv2.rectangle(clone, rects[-1][0], rects[-1][1], (0, 255, 0), 2)  # Dibuja el rectángulo
                cv2.imshow("Selecciona Áreas", clone)

        cv2.namedWindow("Selecciona Áreas")
        cv2.setMouseCallback("Selecciona Áreas", click_and_crop)

        while True:
            cv2.imshow("Selecciona Áreas", clone)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):  # Presiona 'q' para salir
                break

        cv2.destroyAllWindows()
        return rects, image






