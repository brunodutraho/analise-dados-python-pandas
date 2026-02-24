import sqlite3

# 1 - Conectando no BD
conexao = sqlite3.connect('titulo.db')

# 2 - Criando cursor para manipular o BD
cursor = conexao.cursor()

# 3 - Criando tabela com os campos id, titulo e autor
cursor.execute(
    """CREATE TABLE filmes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    ano INTEGER NOT NULL,
    nota REAL NOT NULL
    )"""
)

# 4 - Fechando a conexão com o BD
conexao.close()
print('Tabela criada com sucesso!')