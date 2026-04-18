numeros = set([1,2,3,1,2,4])
print(numeros)

abacaxi = set("abacaxi")
print(abacaxi)

carros = set(("gol", "celta", "palio", "gol", "celta", "palio"))
print(carros)

#consultor do set serve para elimizar duplicidade na lista seja de letras ou se tiver conjuntos de que não tenha demais objetos duplicados

linguagens = {"python", "java", "python"} #pode ser ativo por chaves o set, não precisando declarar o mesmo como: set({}) e usando só {}
print(linguagens)

for indice, linguagem in enumerate(linguagens):
    print(f"indice: {indice}, linguagem: {linguagem}")

for linguagem in linguagens:
    print(linguagem)

# ele só pode ser usado como iteravel através de for para percorrer esse iterador 

# pop em conjuntos sempre tirar o primeiro valor


"""
linguagens = list(linguagens)
print(linguagens[0]
"""




"""
O Python usa chaves { } para duas estruturas diferentes. O que define qual será criada é o que você coloca dentro delas:

Dicionário: Se houver pares de chave: valor (ex: {"nome": "Python"}).

Set (Conjunto): Se houver apenas valores soltos (ex: {"python", "java"}).

conjuntos não fazem fatiamente e nem indexação por issp é complicado pedir algo em especifico, somente convertendo em lista
"""