"""Roda a mesma tarefa em Pandas e Polars e mede o tempo de cada etapa."""
import time

import pandas as pd
import polars as pl

tempos = []


def medir(etapa, biblioteca, func):
    inicio = time.perf_counter()
    resultado = func()
    tempos.append((etapa, biblioteca, time.perf_counter() - inicio))
    return resultado


# Ler
df_pd = medir("ler csv", "pandas", lambda: pd.read_csv("dados/vendas.csv"))
df_pl = medir("ler csv", "polars", lambda: pl.read_csv("dados/vendas.csv"))
lojas_pd = pd.read_csv("dados/lojas.csv")
lojas_pl = pl.read_csv("dados/lojas.csv")

# Filtrar
f_pd = medir("filtrar", "pandas", lambda: df_pd[df_pd["valor"] > 100])
f_pl = medir("filtrar", "polars", lambda: df_pl.filter(pl.col("valor") > 100))

# Agrupar
g_pd = medir("agrupar", "pandas", lambda: f_pd.groupby("loja_id", as_index=False)["valor"].sum())
g_pl = medir("agrupar", "polars", lambda: f_pl.group_by("loja_id").agg(pl.col("valor").sum()))

# Juntar
j_pd = medir("join", "pandas", lambda: g_pd.merge(lojas_pd, on="loja_id"))
j_pl = medir("join", "polars", lambda: g_pl.join(lojas_pl, on="loja_id"))

# Gravar
medir("gravar parquet", "pandas", lambda: f_pd.to_parquet("dados/saida_pandas.parquet"))
medir("gravar parquet", "polars", lambda: f_pl.write_parquet("dados/saida_polars.parquet"))

# Bônus → modo lazy do Polars: o plano inteiro otimizado de uma vez
medir("tudo (lazy)", "polars", lambda: (
    pl.scan_csv("dados/vendas.csv")
    .filter(pl.col("valor") > 100)
    .group_by("loja_id").agg(pl.col("valor").sum())
    .join(lojas_pl.lazy(), on="loja_id")
    .collect()
))

print(f"\n{'etapa':<16}{'pandas':>10}{'polars':>10}")
etapas = dict.fromkeys(t[0] for t in tempos)
for etapa in etapas:
    pd_t = next((t for e, b, t in tempos if e == etapa and b == "pandas"), None)
    pl_t = next((t for e, b, t in tempos if e == etapa and b == "polars"), None)
    fmt = lambda x: f"{x:.3f}s" if x is not None else "n/a"
    print(f"{etapa:<16}{fmt(pd_t):>10}{fmt(pl_t):>10}")
