# ConvertorFac: Software de Gestión y Procesamiento de Cotizaciones

**ConvertorFac** es una herramienta diseñada para gestionar, procesar y consolidar cotizaciones provenientes de archivos PDF o imágenes escaneadas. Este software combina capacidades de extracción de datos mediante OCR y procesamiento estructurado, brindando una interfaz gráfica intuitiva para analizar, editar y exportar datos de manera eficiente.

## Funcionalidades Principales

- **Modo Automático**: Procesa automáticamente archivos PDF con estructuras bien definidas, extrayendo columnas clave como `Código`, `Descripción`, `Unidad` y `Precio`.
- **Modo Manual**: Permite al usuario seleccionar columnas relevantes cuando los encabezados o estructuras no son estándar, ofreciendo flexibilidad en la configuración.
- **OCR para Cotizaciones Escaneadas**: Utiliza reconocimiento óptico de caracteres (OCR) para procesar imágenes escaneadas de cotizaciones, con herramientas para seleccionar y mapear áreas específicas de interés.
- **Edición Interactiva**: Una tabla integrada permite:
  - Visualizar los datos extraídos.
  - Eliminar filas seleccionadas.
  - Limpiar la tabla completa con un solo clic.
- **Exportación a Excel**: Los datos procesados pueden ser exportados a un archivo Excel, permitiendo agregar información a un archivo existente o crear uno nuevo.
- **Formateo de Excel**: Convierte archivos Excel existentes al formato ConstrucData con un solo clic.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal del proyecto.
- **Tkinter**: Para la interfaz gráfica de usuario.
- **Pandas**: Procesamiento y manipulación de datos.
- **Pytesseract**: Para la extracción de texto desde imágenes (OCR).
- **Pillow**: Manipulación de imágenes.
- **pdfplumber**: Extracción de datos tabulares desde archivos PDF.
- **OpenCV**: Selección y preprocesamiento de áreas en imágenes escaneadas.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Lukreynol01/ConvertorFac.git
   ```
2. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegúrate de que **Tesseract OCR** esté instalado en tu sistema y configurado correctamente. Puedes descargarlo desde [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso

1. Abre la aplicación e importa tus cotizaciones:
   - En **modo automático**, selecciona PDFs bien estructurados para una extracción rápida.
   - En **modo manual**, ajusta los encabezados o mapea columnas según sea necesario.
2. Utiliza la funcionalidad OCR para procesar cotizaciones escaneadas desde imágenes.
3. Revisa y edita los datos en la tabla integrada.
4. Exporta los datos procesados a un archivo Excel.
5. Si ya cuentas con un Excel y deseas adaptarlo al formato ConstrucData, pulsa **Formatear Excel**, elige el archivo de origen y la ruta donde se guardará el resultado.

## Capturas de Pantalla

![ConvertorFac Interfaz](https://github.com/Lukreynol01/ConvertorFac/blob/main/Captura%20de%20pantalla%202025-01-16%20223605.png)


## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este software, siéntete libre de abrir un **issue** o enviar un **pull request**.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

