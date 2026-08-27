import pandas as pd
import matplotlib.pyplot as plt

df_stream = pd.read_csv("streamdata_usuarios.csv")

print("Primeiras 5 linhas:")
print(df_stream.head())

print("\nInformações do DataFrame:")
df_stream.info()

#tarefa 2

media_horas_por_plano = df_stream.groupby("plano")["horas_assistidas"].mean().sort_values()

print("\nMédia de horas assistidas por plano:")
print(media_horas_por_plano)

plt.figure(figsize=(8, 5))
plt.barh(media_horas_por_plano.index, media_horas_por_plano.values, color="mediumseagreen")
plt.title("Média de Horas Assistidas por Plano de Assinatura")
plt.xlabel("Média de Horas Assistidas")
plt.ylabel("Plano")
plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

#tarefa 3

cancelaram = df_stream[df_stream["cancelou_assinatura"] == "Sim"]
ativos = df_stream[df_stream["cancelou_assinatura"] == "Não"]

plt.figure(figsize=(8, 5))
plt.hist(ativos["score_satisfacao"], bins=10, alpha=0.6, label="Ativos (Não cancelou)", color="steelblue")
plt.hist(cancelaram["score_satisfacao"], bins=10, alpha=0.6, label="Cancelou", color="indianred")
plt.title("Distribuição da Satisfação: Cancelados vs Ativos")
plt.xlabel("Score de Satisfação")
plt.ylabel("Número de Usuários")
plt.legend()
plt.tight_layout()
plt.show()

#tarefa 4

contagem_dispositivos = df_stream["dispositivo_principal"].value_counts()
print("\nContagem de usuários por dispositivo:")
print(contagem_dispositivos)

dispositivo_mais_usado = contagem_dispositivos.idxmax()
explode = [0.1 if disp == dispositivo_mais_usado else 0 for disp in contagem_dispositivos.index]

plt.figure(figsize=(7, 7))
plt.pie(
    contagem_dispositivos.values,
    labels=contagem_dispositivos.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=explode,
    colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"],
    wedgeprops={"width": 0.6}
)
plt.title("Distribuição dos Dispositivos Principais dos Assinantes")
plt.axis("equal")
plt.tight_layout()
plt.show()