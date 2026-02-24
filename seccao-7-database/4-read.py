import sqlite3

# 1 - Conectando no BD
conexao = sqlite3.connect('titulo.db')
cursor = conexao.cursor()

# 2 - Lendo os dados da tabela
dados = cursor.execute("SELECT * FROM filmes")

# 3 - Imprimindo os dados
print(dados.fetchall())