import pandas as pd
from conexao_post import get_connection


def get_all_games():
    conn = get_connection()

    try:
        query = "SELECT * FROM games"
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None

    finally:
        conn.close()


if __name__ == "__main__":
    df_games = get_all_games()
    print(df_games)