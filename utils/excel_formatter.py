"""Utilities to format raw Excel exports into ConstrucData format."""

from __future__ import annotations

from typing import List

import pandas as pd

from .construcdata_parser import parse_rows
from .excel_handler import export_to_excel


def _load_rows_from_excel(input_path: str) -> List[List[str]]:
    """Load *input_path* and return its contents as a list of string rows.

    The function uses :func:`pandas.read_excel` without header assumption and
    fills missing values with empty strings so that the parser can operate on
    uniform data.
    """

    df = pd.read_excel(input_path, header=None).fillna("")
    return df.astype(str).values.tolist()


def format_to_construcdata(input_path: str, output_path: str) -> None:
    """Convert *input_path* Excel file to ConstrucData format.

    The source Excel is parsed using the existing card parser and the resulting
    structured data is exported through :func:`export_to_excel`.
    """

    rows = _load_rows_from_excel(input_path)
    cards = parse_rows(rows)

    data = [
        [
            card.get("clave", ""),
            card.get("descripcion", ""),
            card.get("unidad", ""),
            card.get("jornada", ""),
            card.get("rendimiento", ""),
        ]
        for card in cards
    ]
    resources = [card.get("recursos", []) for card in cards]
    export_to_excel(data, resources, output_path)
