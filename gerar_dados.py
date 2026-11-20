"""Gera dados/vendas.csv (1 milhão de linhas) e dados/lojas.csv."""
from pathlib import Path

import numpy as np
import pandas as pd

LINHAS = 1_000_000
rng = np.random.default_rng(42)
Path("dados").mkdir(exist_ok=True)

vendas = pd.DataFrame({
    "venda_id": np.arange(LINHAS),
    "loja_id": rng.integers(1, 51, LINHAS),
    "produto": rng.choice(["Notebook", "Mouse", "Monitor", "Cadeira", "Mesa"], LINHAS),
    "valor": rng.uniform(10, 5000, LINHAS).round(2),
})
vendas.to_csv("dados/vendas.csv", index=False)

lojas = pd.DataFrame({
    "loja_id": range(1, 51),
    "cidade": rng.choice(["Recife", "Salvador", "Curitiba", "São Paulo"], 50),
})
lojas.to_csv("dados/lojas.csv", index=False)

print(f"Gerado → {LINHAS:,} vendas e 50 lojas em dados/")
