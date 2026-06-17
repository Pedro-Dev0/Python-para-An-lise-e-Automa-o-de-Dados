from flask import Flask

app = Flask(__name__)
# coloque poetry env info no terminal para colocar interpretador o env criado

@app.route("/") # rota só com / é porque não tem caminho feito, seria como ir para home, demais rotas para locais especificos
def hello_world():
    return "<p>Hello, World!</p>"
# para rodar use no terminal ' poetry run flask --app app run para ativar o ambiente virtual / poetry run flask --app app run --debug (modo debug)



