# Formateador de ConstrucData

Aplicación de escritorio para convertir archivos Excel al formato aceptado por el importador de ConstrucData. Permite cargar un Excel con tarjetas de análisis de precios unitarios, visualizarlo, realizar ediciones simples y exportar el resultado final.

## Funcionalidades Principales

- **Carga de Excel**: Importa un archivo `.xls` o `.xlsx` sin formato y lo muestra en la tabla.
- **Formateo**: Convierte el archivo cargado al esquema requerido por ConstrucData (`Clave`, `Descripción`, `Unidad`, `Jornada`, `Rendimiento`, `Insumos/Recursos`).
- **Edición Interactiva**: La tabla permite eliminar filas, limpiar todos los datos o editar la columna de recursos con un doble clic.
- **Exportación**: Los datos mostrados pueden anexarse a un archivo Excel existente.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal del proyecto.
- **Tkinter**: Interfaz gráfica de usuario.
- **Pandas**: Manipulación y escritura de archivos Excel.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Lukreynol01/ConvertorFac.git
   ```
2. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso

1. Haz clic en **Cargar Archivo Excel** para seleccionar el documento original.
2. Presiona **Formatear Excel** y elige dónde guardar el resultado formateado. El contenido generado se mostrará en la tabla.
3. Opcionalmente, usa **Exportar a Excel** para anexar los datos actuales a otro archivo.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

