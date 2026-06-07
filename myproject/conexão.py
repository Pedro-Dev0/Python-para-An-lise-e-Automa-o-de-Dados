import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / 'clientes.db')
print(conexao)
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

atualizar_dados(conexao, cursor, 'Pedro Henrique', 'pedro123@gmail.com', 1)
atualizar_dados(conexao, cursor, 'Jessica Zacarias', 'jessicazaca123@gmail.com', 2)



