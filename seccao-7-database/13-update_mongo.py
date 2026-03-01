from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pprint import pprint

try:
    client = MongoClient("mongodb://localhost:27017/")
    client.admin.command("ping")
    print("Conectado ao MongoDB.")

    db = client["dbposts"]
    collection = db["posts"]

    filtro = {"level": "Avançado"}
    atualizacao = {"$set": {"level": "Iniciante"}}

    resultado = collection.update_one(filtro, atualizacao)

    print(f"\nDocumentos encontrados: {resultado.matched_count}")
    print(f"Documentos modificados: {resultado.modified_count}\n")

    for doc in collection.find():
        pprint(doc)

except ConnectionFailure:
    print("Erro ao conectar no MongoDB.")

finally:
    client.close()