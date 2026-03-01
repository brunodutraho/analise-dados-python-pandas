from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pprint import pprint

try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command("ping")
    print("Conectado ao MongoDB.")

    db = client["dbposts"]
    collection = db["posts"]

    filtro = {"category": "Backend"}

    resultado = collection.delete_one(filtro)

    print(f"\nDocumentos encontrados para deletar: {resultado.deleted_count}\n")

    print("Documentos restantes na coleção:\n")
    for doc in collection.find():
        pprint(doc)

except ConnectionFailure:
    print("Erro ao conectar ao MongoDB.")

finally:
    client.close()