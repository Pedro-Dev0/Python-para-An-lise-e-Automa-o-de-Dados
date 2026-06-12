import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent
# ROOT_PATH usado para inclinar o banco a ser criado na mesma pasta onde está o código(tem que importar pathlib caso não tenha installe)

# conexao usado para criar o banco caso não tenha e se tiver para conectar aqui a esse código para desenvolvimento do mesmo
conexao = sqlite3.connect(ROOT_PATH / 'clientes.db')
print(conexao)

#cursor para executar ações aqui no código e essas ações serem incluidas no arquivo db
cursor = conexao.cursor()
print(cursor)

def criar_tabela(conexao, cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE)')
    conexao.commit()
    cursor.close()
    conexao.close()


def inserir_dados(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute('INSERT INTO clientes (nome, email) VALUES (?,?);', (data))
    conexao.commit()

def atualizar_dados(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute('UPDATE clientes SET nome=?, email=? WHERE id=?;', (data))
    conexao.commit()

def deletar_dados(conexao, cursor, id):
    data = (id,)
    cursor.execute('DELETE FROM clientes WHERE id=?;', (data))
    conexao.commit()




'''
atualizar_dados(conexao, cursor, 'Pedro Henrique', 'pedro123@gmail.com', 1)
atualizar_dados(conexao, cursor, 'Jessica Zacarias', 'jessicazaca123@gmail.com', 2)
'''

#inserir_dados(conexao, cursor, 'PEDRIMZL', 'ISA@GMAIL.COM')

#deletar_dados(conexao, cursor, 3)





