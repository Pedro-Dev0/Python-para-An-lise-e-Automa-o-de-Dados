from flask import Flask, url_for

app = Flask(__name__)
# coloque poetry env info no terminal para colocar interpretador o env criado

@app.route("/olamundo/<usuario>/<int:idade>/<float:altura>") # rota só com / é porque não tem caminho feito, seria como ir para home, demais rotas para locais especificos
def hello_world(usuario, idade, altura):
    print(idade)
    print(altura)
    print(f'tipo da variavel idade: {type(idade)}')
    print(f'tipo da variavel usuario: {type(usuario)}')
    print(f'tipo da variavel altura: {type(altura)}')
    return f"<p>Hello, World! {usuario}</p>"  # adicionamos mais variaveis porém primeiro o tipo <int:idade> após isso a variavel ou dado na rota

# se mudar de pasta use após --app nomedapasta.app run --debug(se quiser debug)(isso leva em conta que esteja uma pasta anterior ou depois da pasta principal)
# para rodar use no terminal ' poetry run flask --app app run para ativar o ambiente virtual / poetry run flask --app app run --debug (modo debug)

@app.route("/bemvindo/")
def bem_vindo():
    return "<p>Bem vindo!</p>"
# com barra no final da route tem redirecionamento sem barra não tem e se for colocada da um erro 404

with app.test_request_context():
    print(url_for("bem_vindo", next="/"))
    print(url_for("hello_world", usuario='Pedro', idade=23, altura=1.70))



