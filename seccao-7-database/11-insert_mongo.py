from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient('mongodb://localhost:27017/')
    client.admin.command('ping')
    print("Conectado ao MongoDB com sucesso!")

    mydb = client.dbposts
    mycollection = mydb.posts

    post1 = {
        "title": "FastAPI",
        "category": "Backend",
        "level": "Intermediário",
        "author": {
            "name": "Bruno",
            "email": "bruno@example.com"
        }
    }

    result = mycollection.insert_one(post1)
    print("ID do documento inserido:", result.inserted_id)

except ConnectionFailure:
    print("Não foi possível conectar ao MongoDB.")