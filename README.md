# ConvertorFac
ConvertorFac: Software de Gestión y Procesamiento de Cotizaciones

ConvertorFac es una herramienta diseñada para gestionar, procesar y consolidar cotizaciones provenientes de archivos PDF o imágenes escaneadas. Este software combina capacidades de extracción de datos mediante OCR y procesamiento estructurado, brindando una interfaz gráfica intuitiva para analizar, editar y exportar datos de manera eficiente.

Funcionalidades Principales
Modo Automático: Procesa automáticamente archivos PDF con estructuras bien definidas, extrayendo columnas clave como Código, Descripción, Unidad y Precio.
Modo Manual: Permite al usuario seleccionar columnas relevantes cuando los encabezados o estructuras no son estándar, ofreciendo flexibilidad en la configuración.
OCR para Cotizaciones Escaneadas: Utiliza reconocimiento óptico de caracteres (OCR) para procesar imágenes escaneadas de cotizaciones, con herramientas para seleccionar y mapear áreas específicas de interés.
Edición Interactiva: Una tabla integrada permite:
Visualizar los datos extraídos.
Eliminar filas seleccionadas.
Limpiar la tabla completa con un solo clic.
Exportación a Excel: Los datos procesados pueden ser exportados a un archivo Excel, permitiendo agregar información a un archivo existente o crear uno nuevo.
Tecnologías Utilizadas
Python: Lenguaje principal del proyecto.
Tkinter: Para la interfaz gráfica de usuario.
Pandas: Procesamiento y manipulación de datos.
Pytesseract: Para la extracción de texto desde imágenes (OCR).
Pillow: Manipulación de imágenes.
pdfplumber: Extracción de datos tabulares desde archivos PDF.
OpenCV: Selección y preprocesamiento de áreas en imágenes escaneadas.
Instalación
Clona este repositorio:

bash
Copiar
Editar
git clone https://github.com/tuusuario/ConvertorFac.git
Instala las dependencias requeridas:

bash
Copiar
Editar
pip install -r requirements.txt
Asegúrate de que Tesseract OCR esté instalado en tu sistema y configurado correctamente. Puedes descargarlo desde Tesseract OCR.

Ejecuta la aplicación:

bash
Copiar
Editar
python main.py
Uso
Abre la aplicación e importa tus cotizaciones:
En modo automático, selecciona PDFs bien estructurados para una extracción rápida.
En modo manual, ajusta los encabezados o mapea columnas según sea necesario.
Utiliza la funcionalidad OCR para procesar cotizaciones escaneadas desde imágenes.
Revisa y edita los datos en la tabla integrada.
Exporta los datos procesados a un archivo Excel.
Capturas de Pantalla



Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este software, siéntete libre de abrir un issue o enviar un pull request.

Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
