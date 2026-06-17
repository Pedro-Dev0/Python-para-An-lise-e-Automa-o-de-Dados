from flask import Flask

app = Flask(__name__)
# coloque poetry env info no terminal para colocar interpretador o env criado
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
# para rodar use no terminal ' poetry run flask --app app run para ativar o ambiente virtual

