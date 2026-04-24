"""import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

plt.plot(x, y)
plt.show()"""

import pandas as pd

arquivo = (r"C:\Users\suporte\Downloads\ControleD pontoE fsense.xlsx")

df = pd.read_excel(arquivo)

print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum()) # verifica os valores ausentes e como podemos ver mostra o valor ausente...

df_limpo = df.dropna() # para limpar partes ausentes que podem gera problema
print(df_limpo.isnull().sum())
print(df_limpo.head())
print(df_limpo.info())
print(df_limpo.describe())


