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

def cadastrar_laudo(id_paciente, id_medico, data, prescricao):
    resposta_laudo = laudo.insert_one({
        "id_paciente" : id_paciente,
        "id_medico" : id_medico,
        "data" : data,
        "prescricao" : prescricao
    })
    if(resposta_laudo):
        print("Laudo cadastrado!")
    else:
        print("Erro!")
    

def cadastrar_exame(id_paciente, tipo_exame, data, resultado):
    resposta_exame = exame.insert_one({
        "id_paciente" : id_paciente,
        "tipo_exame" : tipo_exame,
        "data" : data,
        "resultado" : resultado
    })
    if(resposta_exame):
        print("Exame cadastrado!")
    else:
        print("Erro!")
    
def consultar_laudo(id_paciente, data):
    resposta_laudo = laudo.find_one({
        "id_paciente" : id_paciente,
        "data" : data
    })
    if(resposta_laudo):
        print(resposta_laudo)
    else:
        print("Erro!")

def consultar_exame(id_paciente, data):
    resposta_exame = exame.find_one({
        "id_paciente" : id_paciente,
        "data" : data
    })
    if(resposta_exame):
        print(resposta_exame)
    else:
        print("Erro!")

cadastrar_laudo(3, 3, "2025-05-23", "corno")
cadastrar_exame(3, "corno", "2025-05-23", "yes")

consultar_laudo(3, "2025-05-23")
consultar_exame(3, "2025-05-23")