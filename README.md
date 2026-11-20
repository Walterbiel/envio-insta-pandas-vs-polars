# Pandas vs Polars

Material gratuito do QG da Engenharia de Dados. Você recebeu porque comentou **POLARS**.

A mesma tarefa nas duas bibliotecas, com o tempo de cada etapa.

## Como usar este material

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Gere a base de teste (1 milhão de linhas):

```bash
python gerar_dados.py
```

3. Rode a comparação:

```bash
python comparar.py
```

4. Abra [comparar.py](comparar.py) → o código de cada etapa está lado a lado

## O fluxo

```
gerar_dados.py → dados/vendas.csv + dados/lojas.csv → comparar.py → tabela de tempos
```

## As etapas comparadas

→ Ler o CSV
→ Filtrar vendas acima de 100
→ Agrupar por loja
→ Juntar com a tabela de lojas
→ Gravar em Parquet

## A mesma operação nos dois

```python
# Pandas
df[df["valor"] > 100].groupby("loja_id")["valor"].sum()

# Polars
df.filter(pl.col("valor") > 100).group_by("loja_id").agg(pl.col("valor").sum())
```

## Quando usar cada um

| | Pandas | Polars |
|---|---|---|
| Velocidade | Boa | Muito boa (multithread) |
| Memória | Usa mais | Usa menos |
| Modo lazy | Não | Sim (`scan_csv`) |
| Ecossistema | Enorme | Crescendo |
| Use quando | Bibliotecas dependem dele, dado pequeno | Dado médio ou grande, pipelines novos |

O resultado muda de máquina para máquina → rode e veja no seu computador.

## QG da Engenharia de Dados

Este material é uma amostra do que você encontra no QG.

→ Trilha completa do zero ao sênior
→ Projetos reais para o portfólio
→ Comunidade para tirar dúvidas

Acesse → [qg-engenharia-de-dados.com.br](https://qg-engenharia-de-dados.com.br)
YouTube → [@gonzagadosdados](https://www.youtube.com/@gonzagadosdados)
