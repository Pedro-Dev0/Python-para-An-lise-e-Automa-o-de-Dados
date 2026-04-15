numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
pares = [numero for numero in numeros if numero % 2 == 0] #compression para fazer code menor
impares = [numero for numero in numeros if numero % 2 != 0]
quadrado = [numero ** 2 for numero in numeros]
dobro = [numero * 2 for numero in numeros if numero > 9]
dobro_par = [numero for numero in numeros if numero >= 20 and numero % 2 == 0]

#  esse != sinal é de desigualdade e é oposto ao de igualdade o ==
print(pares)
print(impares)
print(numeros)
print(quadrado)
print(dobro)
print(dobro_par)


for indice, numero in enumerate(numeros):
    print(f"indice: {indice}, numero: {numero}")


"""
for numero in numeros:
    print(numero)
"""

"""
for numero in numeros:
    if numero % 2 == 0:
        pares.append(numero)
    else:
        impares.append(numero)
"""