import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / 'datasets' / 'vendas.json'

with open(DATASET_PATH, encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

df['Data da Compra'] = pd.to_datetime(
    df['Data da Compra'],
    format='%d/%m/%Y'
)
