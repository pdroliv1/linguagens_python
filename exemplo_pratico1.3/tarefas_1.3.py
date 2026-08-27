df["Faturamento_Total"] = df["Quantidade"] * df["Preco_Unitario"]

faturamento_por_produto = df.groupby("Produto")["Faturamento_Total"].sum().sort_values(ascending=False)

print("Faturamento total por produto:")
print(faturamento_por_produto)

plt.figure(figsize=(8, 5))
plt.bar(faturamento_por_produto.index, faturamento_por_produto.values, color="steelblue")
plt.title("Faturamento Total por Produto")
plt.xlabel("Produto")
plt.ylabel("Faturamento (R$)")
plt.tight_layout()
plt.show()

# tarefa 2

df["Mes"] = df["Data"].dt.to_period("M")

vendas_por_mes = df.groupby("Mes")["Faturamento_Total"].sum().sort_index()

print("\nFaturamento total por mês:")
print(vendas_por_mes)

plt.figure(figsize=(8, 5))
plt.plot(vendas_por_mes.index.astype(str), vendas_por_mes.values, marker="o", color="darkorange")
plt.title("Evolução das Vendas ao Longo do Tempo")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# tarefa 3
quantidade_por_produto = df.groupby("Produto")["Quantidade"].sum()

print("\nQuantidade total vendida por produto:")
print(quantidade_por_produto)

plt.figure(figsize=(7, 7))
plt.pie(
    quantidade_por_produto.values,
    labels=quantidade_por_produto.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
)
plt.title("Distribuição da Quantidade Vendida por Produto")
plt.axis("equal")
plt.tight_layout()
plt.show()