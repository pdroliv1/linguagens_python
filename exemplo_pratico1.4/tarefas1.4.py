n_duplicatas = df_ecommerce.duplicated().sum()
print(f"Número de linhas duplicadas encontradas: {n_duplicatas}")

df_ecommerce = df_ecommerce.drop_duplicates()
print(f"Total de linhas após remoção de duplicatas: {len(df_ecommerce)}")

print("\nValores nulos por coluna:")
print(df_ecommerce.isnull().sum())

mediana_avaliacao = df_ecommerce["Avaliacao_Compra"].median()
print(f"\nMediana de Avaliacao_Compra: {mediana_avaliacao}")

df_ecommerce["Avaliacao_Compra"] = df_ecommerce["Avaliacao_Compra"].fillna(mediana_avaliacao)

print("\nValores nulos após tratamento:")
print(df_ecommerce.isnull().sum())

#tarefa 2

plt.figure(figsize=(9, 6))
sns.boxplot(data=df_ecommerce, x="Categoria", y="Valor_Gasto", palette="Set2")
plt.title("Distribuição do Valor Gasto por Categoria")
plt.xlabel("Categoria")
plt.ylabel("Valor Gasto (R$)")
plt.tight_layout()
plt.show()

variacao_por_categoria = df_ecommerce.groupby("Categoria")["Valor_Gasto"].std().sort_values(ascending=False)
print("Desvio padrão do Valor_Gasto por categoria:")
print(variacao_por_categoria)
print(f"\nCategoria com maior variação: {variacao_por_categoria.index[0]}")

#tarefa 3

plt.figure(figsize=(8, 5))
sns.histplot(data=df_ecommerce, x="Idade_Cliente", kde=True, color="cornflowerblue", bins=15)
plt.title("Distribuição da Idade dos Clientes")
plt.xlabel("Idade do Cliente")
plt.ylabel("Frequência")
plt.tight_layout()
plt.show()