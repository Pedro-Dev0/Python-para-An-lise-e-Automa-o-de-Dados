import csv

total = 0
with open(r'C:\Users\Malleus\Documents\GitHub\Python-para-An-lise-e-Automa-o-de-Dados\Python\revendo conceitos\conceitos\vendas.txt', 'w') as f:
    f.write('100\n200\n150\n300')

with open(r'C:\Users\Malleus\Documents\GitHub\Python-para-An-lise-e-Automa-o-de-Dados\Python\revendo conceitos\conceitos\vendas.txt', 'r') as f:
    for linha in f:
        valor = int(linha.strip())
        total += valor


print(total)

# teste de analise de dados e automação do mesmo