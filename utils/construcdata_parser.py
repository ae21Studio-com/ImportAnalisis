"""Parser for ConstrucData PDF output.

This module processes raw row data extracted from Construction Data
"An\u00e1lisis de Precio Unitario" PDF files and builds structured
representations of each card in the document.

Steps performed:
1. Locate rows containing the marker "AN\u00c1LISIS DE PRECIO UNITARIO" to
   delimit each card.
2. The following line is interpreted as the master concept
   (``clave``, ``descripcion`` and ``unidad``).
3. Subsequent rows are scanned until a blank line or the next marker is
   reached. Rows whose first column looks like a resource key are
   accumulated as resources. Rows containing the words ``JORNADA`` or
   ``RENDIMIENTO`` are used to capture those values.

The main public function is :func:`parse_pdf` which accepts a PDF path and
returns a list of dictionaries with the following keys:
``clave``, ``descripcion``, ``unidad``, ``jornada``, ``rendimiento`` and
``recursos``.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional

from .pdf_parser import extract_data_from_pdf


def _is_resource_key(value: str) -> bool:
    """Return ``True`` if *value* looks like a resource key.

    The heuristic considers alphanumeric strings (optionally containing
    dashes or dots) as resource keys.
    """

    return bool(re.match(r"^[A-Z0-9][A-Z0-9.-]*$", value))


def _parse_resource(row: List[str]) -> Dict[str, str]:
    """Parse a resource row into a dictionary.

    The number of columns in the raw data may vary; this function tries to
    map the most common five-column layout:
    ``clave``, ``descripcion``, ``unidad``, ``cantidad`` and ``precio``.
    Any missing fields are filled with an empty string.
    """

    if len(row) > 4:
        descripcion = " ".join(row[1:-3]).strip()
    elif len(row) > 2:
        descripcion = " ".join(row[1:-2]).strip()
    elif len(row) > 1:
        descripcion = row[1].strip()
    else:
        descripcion = ""

    recurso: Dict[str, str] = {
        "clave": row[0].strip() if row else "",
        "descripcion": descripcion,
        "unidad": row[-3].strip() if len(row) >= 3 else "",
        "cantidad": row[-2].strip() if len(row) >= 2 else "",
        "precio": row[-1].strip() if row else "",
    }
    return recurso


def parse_rows(data: Iterable[List[str]]) -> List[Dict[str, Any]]:
    """Parse iterable *data* of rows into structured cards.

    Each element of *data* must be a sequence of strings representing a
    table row.  The function returns a list of dictionaries describing each
    card found in the data.
    """

    tarjetas: List[Dict[str, Any]] = []
    rows = list(data)
    i = 0
    while i < len(rows):
        row = rows[i]
        row_text = " ".join(row)
        if "ANÁLISIS DE PRECIO UNITARIO" in row_text:
            if i + 1 >= len(rows):
                break
            concept_row = rows[i + 1]
            clave = concept_row[0].strip() if concept_row else ""
            unidad = concept_row[-1].strip() if len(concept_row) > 2 else ""
            descripcion = " ".join(concept_row[1:-1]).strip() if len(concept_row) > 2 else ""

            j = i + 2
            recursos: List[Dict[str, str]] = []
            jornada: Optional[str] = None
            rendimiento: Optional[str] = None

            while j < len(rows):
                current = rows[j]
                current_text = " ".join(current)
                if not any(cell.strip() for cell in current):
                    # blank line signals end of card
                    j += 1
                    break
                if "ANÁLISIS DE PRECIO UNITARIO" in current_text:
                    break

                if "JORNADA" in current:
                    try:
                        idx = current.index("JORNADA")
                        if idx + 1 < len(current):
                            jornada = current[idx + 1].strip()
                    except ValueError:
                        pass
                    if "RENDIMIENTO" in current:
                        idx = current.index("RENDIMIENTO")
                        if idx + 1 < len(current):
                            rendimiento = current[idx + 1].strip()
                    j += 1
                    continue

                first = current[0].strip()
                if _is_resource_key(first):
                    recursos.append(_parse_resource(current))
                j += 1

            tarjetas.append(
                {
                    "clave": clave,
                    "descripcion": descripcion,
                    "unidad": unidad,
                    "jornada": jornada,
                    "rendimiento": rendimiento,
                    "recursos": recursos,
                }
            )
            i = j
        else:
            i += 1
    return tarjetas


def parse_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Convenience wrapper that loads *pdf_path* and parses its content."""

    raw_data = extract_data_from_pdf(pdf_path)
    return parse_rows(raw_data)

