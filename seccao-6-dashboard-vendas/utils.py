import os
from pathlib import Path


def load_all_css(folder_path: str = "styles") -> str:
    """
    Carrega todos os arquivos .css de uma pasta e retorna
    como string HTML <style>.
    """
    css = ""
    path = Path(folder_path)

    if not path.exists():
        return ""

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
