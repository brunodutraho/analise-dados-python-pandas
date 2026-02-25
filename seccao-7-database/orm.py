from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Criação do engine
engine = create_engine("sqlite:///banco.db", echo=False)

Base = declarative_base()

# Modelo
class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    nota = Column(Float, nullable=False)

# Criação das tabelas
Base.metadata.create_all(engine)

# Sessão
Session = sessionmaker(bind=engine)


# CREATE
def adiciona_filme(nome, ano, nota):
    with Session() as session:
        try:
            filme = Filme(nome=nome, ano=ano, nota=nota)
            session.add(filme)
            session.commit()
            return filme.id
        except Exception as e:
            session.rollback()
            print(f"Erro ao adicionar filme: {e}")
            raise


# UPDATE
def atualiza_filme(id, nome=None, ano=None, nota=None):
    with Session() as session:
        try:
            filme = session.get(Filme, id)
            if not filme:
                return False

            if nome is not None:
                filme.nome = nome
            if ano is not None:
                filme.ano = ano
            if nota is not None:
                filme.nota = nota

            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar filme: {e}")
            raise


# DELETE
def deleta_filme(id):
    with Session() as session:
        try:
            filme = session.get(Filme, id)
            if not filme:
                return False

            session.delete(filme)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar filme: {e}")
            raise


# READ
def listar_filmes():
    with Session() as session:
        return session.query(Filme).all()