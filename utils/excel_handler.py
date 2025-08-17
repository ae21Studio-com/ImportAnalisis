import pandas as pd
import json

def export_to_excel(data, resources, output_path):
    """Exporta datos a un archivo de Excel con información de recursos.

    Args:
        data (list): Datos tabulares para exportar. Cada elemento debe
            representar una fila con los campos "Clave", "Descripción",
            "Unidad", "Jornada" y "Rendimiento".
        resources (list): Lista de objetos que representan los
            insumos o recursos asociados. Puede ser una única lista de recursos
            o una lista de listas para asociar recursos a cada fila.
        output_path (str): Ruta del archivo de salida.
    """

    df = pd.DataFrame(
        data,
        columns=[
            "Clave",
            "Descripción",
            "Unidad",
            "Jornada",
            "Rendimiento",
        ],
    )

    if len(resources) == len(data) and not isinstance(resources, (str, bytes)):
        df["Insumos/Recursos"] = [json.dumps(r, ensure_ascii=False) for r in resources]
    else:
        df["Insumos/Recursos"] = json.dumps(resources, ensure_ascii=False)

    df.to_excel(output_path, index=False)
