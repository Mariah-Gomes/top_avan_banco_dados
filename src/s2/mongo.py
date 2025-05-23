#colecao.insert_one({"nome": "Iago", "idade": 24})

#for doc in colecao.find():
#    print(doc)

#usuario = colecao.find_one({"nome": "Iago"})
#print(usuario)

#colecao.update_one({"nome": "Iago"}, {"$set": {"idade": 25}})

#colecao.delete_one({"nome": "Iago"})

from src.s2.mongoConnection import get_mongo_client

db = get_mongo_client()

# Coleções
laudo = db['laudo']
exame = db['exame']

# Insere um dado
laudo.insert_one({"nome": "Iago", "idade": 24})

# Lê os dados
for doc in laudo.find():
    print(doc)