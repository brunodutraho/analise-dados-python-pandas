from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pprint import pprint

try:
    # Conexão explícita
    client = MongoClient("mongodb://localhost:27017/")
    
    # Testa conexão
    client.admin.command("ping")
    print("Conexão com MongoDB estabelecida com sucesso.")

    # Acessa banco e coleção
    db = client["dbposts"]
    collection = db["posts"]

    # Busca todos os documentos
    cursor = collection.find()

    print("\nDocumentos encontrados:\n")

    for document in cursor:
        pprint(document)

except ConnectionFailure:
    print("Erro: Não foi possível conectar ao MongoDB.")

finally:
    client.close()