import sqlite3

conn = sqlite3.connect('dados.db')

cursor = conn.cursor()
'''
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER
);
""")

conn.commit()

print('Tabela criada com sucesso!')
'''
# separação
'''
cursor.execute(
    "INSERT INTO usuarios (nome, idade) VALUES (?,?)",
    ("Pedro", 23)
)

conn.commit()

print('Dados inseridos com sucesso!')
'''
# separação
cursor.execute("SELECT * FROM usuarios")

dados = cursor.fetchall()

for usuario in dados:
    print(usuario)             # para ver usuários na tabela de dados

conn.close()

