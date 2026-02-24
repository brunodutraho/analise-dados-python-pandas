import sqlite3

# 1 - Conectando ao BD
conexao = sqlite3.connect('titulo.db')
cursor = conexao.cursor()

# 2 - Inserindo dados na tabela
cursor.execute(
    """
        INSERT INTO filmes (nome, ano, nota)
        VALUES ('Sonic', 2020, 8.0)
    """
)

# 3 - Salvando as alterações no BD
conexao.commit()
conexao.close()
print('Dados inseridos com sucesso!')