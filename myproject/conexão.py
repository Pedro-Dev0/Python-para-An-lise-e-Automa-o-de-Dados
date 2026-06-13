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
    cursor.execute('INSERT INTO clientes (nome, email) VALUES (?,?);', (data,))
    conexao.commit()

def atualizar_dados(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute('UPDATE clientes SET nome=?, email=? WHERE id=?;', (data,))
    conexao.commit()

def deletar_dados(conexao, cursor, id):
    data = (id,)
    cursor.execute('DELETE FROM clientes WHERE id=?;', (data,))
    conexao.commit()

def inserir_varios_dados(conexao, cursor, lista):
    cursor.executemany('INSERT INTO clientes (nome, email) VALUES (?,?);', lista)
    conexao.commit()

def recuperar_cliente(conexao, cursor, id):
    data = (id,)
    cursor.execute('SELECT * FROM clientes WHERE id=?;', (data,))
    result = cursor.fetchone()
    print(result)
    conexao.commit()

def listar_clientes(conexao, cursor):
    cursor.execute('SELECT * FROM clientes;')
    result = cursor.fetchall()
    print(result)
    conexao.commit()

listar_clientes(conexao, cursor)





'''
def listar_clientes(conexao, cursor):
    cursor.row_factory = sqlite3.Row # padrao e após isso print com dict para converter em dicionario(nesse exemplo deu errado)
    cursor.execute('SELECT * FROM clientes;')
    result = cursor.fetchall()
    print(dict(result))
    conexao.commit()

'''





'''
atualizar_dados(conexao, cursor, 'Pedro Henrique', 'pedro123@gmail.com', 1)
atualizar_dados(conexao, cursor, 'Jessica Zacarias', 'jessicazaca123@gmail.com', 2)
'''

#inserir_dados(conexao, cursor, 'PEDRIMZL', 'ISA@GMAIL.COM')

#deletar_dados(conexao, cursor, 3)

'''
lista = [
    ('isa', 'isa@gmail.com'),
    ('pedro', 'pedro@gmail.com'),
    ('jessica', 'jessica@gmail.com')
]

inserir_varios_dados(conexao, cursor, lista)
'''



# parte prática de segurança em SQL evite concatenação e consultar parametrizadas