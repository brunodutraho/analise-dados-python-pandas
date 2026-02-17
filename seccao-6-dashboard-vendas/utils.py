import os
from pathlib import Path
import pandas as pd

def load_all_css(folder_path: str = "styles") -> str:
    
    base_path = Path(__file__).parent
    path = base_path / folder_path

    if not path.exists():
        return f"<!-- Pasta {path} não encontrada -->"

    css = ""
    for file in sorted(path.glob("*.css")):
        css += file.read_text(encoding="utf-8")

    return f"<style>{css}</style>"


def format_number(value: float, prefix: str = "") -> str:
    """
    Formata números grandes para padrão brasileiro:
    1.500,00 | 1,5 mil | 2,3 milhões
    """
    abs_value = abs(value)

    if abs_value >= 1_000_000:
        formatted = f"{value / 1_000_000:,.2f} milhões"
    elif abs_value >= 1_000:
        formatted = f"{value / 1_000:,.2f} mil"
    else:
        formatted = f"{value:,.2f}"

    return (
        prefix +
        formatted
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def format_currency_full(value: float, prefix: str = "R$ ") -> str:
    return prefix + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_date_br(value) -> str:
    """
    Formata datetime para padrão brasileiro (dd/mm/yyyy)
    sem exibir hora.
    """
    if pd.isna(value):
        return ""
    return value.strftime("%d/%m/%Y")
