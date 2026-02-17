from pathlib import Path
import pandas as pd

from pathlib import Path

from pathlib import Path

from pathlib import Path

def load_all_css() -> str:
    """
    Carrega todos os arquivos CSS da pasta 'styles' que deve estar 
    no mesmo diretório que este arquivo utils.py.
    """
    # Path(__file__) é o caminho completo do utils.py
    # .parent é a pasta 'seccao-6-dashboard-vendas'
    base_path = Path(__file__).parent.absolute()
    styles_path = base_path / "styles"

    if not styles_path.exists():
        # Debug para você ver no log do Streamlit se ele ainda falhar
        print(f"ERRO: Pasta de estilos não encontrada em: {styles_path}")
        return f"<!-- Pasta {styles_path} não encontrada -->"

    css_content = []
    
    # Busca arquivos .css dentro da pasta styles
    for file in sorted(styles_path.glob("*.css")):
        try:
            # Garante a leitura com encoding utf-8 para evitar erro com acentos
            css_content.append(file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Erro ao ler arquivo {file.name}: {e}")

    if not css_content:
        return "<!-- Nenhum arquivo CSS encontrado na pasta -->"

    # Junta tudo e retorna
    css_string = "\n".join(css_content)
    return f"<style>\n{css_string}\n</style>"




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
