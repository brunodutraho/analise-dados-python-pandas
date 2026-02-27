from conexao_post import get_connection


def delete_game(id):
    conn = get_connection()
    cursor_obj = conn.cursor()

    try:
        cursor_obj.execute(
            """
            DELETE FROM games
            WHERE id = %s
            """,
            (id,)
        )

        conn.commit()
        print("Jogo removido com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao remover jogo: {e}")

    finally:
        cursor_obj.close()
        conn.close()


if __name__ == "__main__":
    delete_game(3)