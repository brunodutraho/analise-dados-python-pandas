import sqlite3

# 1 - Conectando no BD
conexao = sqlite3.connect('titulo.db')
cursor = conexao.cursor()

# 2 - Atualizando um registro
cursor.execute(
    """
        UPDATE filmes SET nota = ? 
        WHERE id = ?
    """,
    (8.5, 4)
)
conexao.commit()

print("Registro atualizado com sucesso!")