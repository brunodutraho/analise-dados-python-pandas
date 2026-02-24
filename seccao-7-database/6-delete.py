import sqlite3

# Conectando no BD
conexao = sqlite3.connect('titulo.db')
cursor = conexao.cursor()

# Deletando um registro
id = (2, 4)
cursor.execute(
    """
        DELETE FROM filmes
        WHERE ID IN (?, ?)
    """,
    id
)

conexao.commit()
print("Registro deletado com sucesso!")