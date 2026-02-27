from conexao_post import get_connection


def update_game_name(new_name, new_id):
    conn = get_connection()
    cursor_obj = conn.cursor()

    try:
        cursor_obj.execute(
            """
            UPDATE games
            SET NAME = %s
            WHERE ID = %s
            """,
            (new_name, new_id)
        )

        conn.commit()
        print("Jogo atualizado com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar jogo: {e}")

    finally:
        cursor_obj.close()
        conn.close()


if __name__ == "__main__":
    update_game_name("Fifa 26", 3)