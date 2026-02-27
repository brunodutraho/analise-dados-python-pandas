from conexao_post import get_connection

def insert_games():
    conn = get_connection()
    cursor_obj = conn.cursor()

    games = [
        ('The Last of Us Part II', 2020, 9.8),
        ('Spider Man: Miles Morales', 2020, 8.5),
        ('Cyberpunk 2077', 2020, 7.0),
        ('Ghost of Tsushima', 2020, 9.5),
        ('Hades', 2020, 9.0)
    ]

    try:
        for game in games:
            cursor_obj.execute(
                """
                INSERT INTO games(name, year, score)
                VALUES (%s, %s, %s)
                """,
                game
            )

        conn.commit()
        print("Dados inseridos com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir dados: {e}")

    finally:
        cursor_obj.close()
        conn.close()


if __name__ == "__main__":
    insert_games()