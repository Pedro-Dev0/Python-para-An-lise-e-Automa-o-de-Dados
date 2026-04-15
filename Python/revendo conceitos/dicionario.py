pessoa = {"nome": "Pedro", "idade": 25}
print(pessoa)
print(pessoa["nome"])

pessoa_1 = dict(nome="Pedro", idade=26)
print(pessoa_1)
print(pessoa_1["nome"])
# essas são as duas formas de se iniciar um dicionario ou pela construtor dict([]) ou atraves de {"chave": "valor",} ou atraves de chave e valor desse jeito simplificado

pessoa["telefone"] = "3333-1234"
pessoa_1["E-mail"] = "pedrim@gmail.com" 
#forma para adicionar alguma informação nova aquele dicionario já criado

print(pessoa)
print(pessoa_1)

pessoas = {
    "Pedro":{"nome": "Pedro", "idade": 25},
    "Maria":{"nome": "Maria", "idade":23},
    "Pedrita":{"nome": "Pedrita", "idade":22},
}

#print(pessoas)
print(pessoas["Pedro"])
print(pessoas["Pedro"]["nome"])


for chave, valor in pessoas.items():
    print(chave, valor) # melhor jeito de passar pela iteração do dicionarios