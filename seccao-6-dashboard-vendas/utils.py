# Leitura dos arquivos CSS
import os
def load_all_css(folder_path="styles"):
    css = ""
    for file in os.listdir(folder_path):
        if file.endswith(".css"):
            with open(os.path.join(folder_path, file), encoding="utf-8") as f:
                css += f.read()
    return f"<style>{css}</style>"

# Formatação de valores monetários    
def format_number(value, prefix = ''):
    for unit in ['', 'mil']:
        if value < 1000:
            return f'{prefix}{value:,.2f}{unit}'.strip()
        value /= 1000
    return f'{prefix}{value:,.2f} milhões'
