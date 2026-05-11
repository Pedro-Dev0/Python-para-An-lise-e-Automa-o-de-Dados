import requests

url = 'https://api.agify.io/?name=murilo'

resposta = requests.get(url)

dados = resposta.json()

print(dados)