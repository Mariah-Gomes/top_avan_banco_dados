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

def cadastrar_laudo(dados):
    resposta_laudo = laudo.insert_one({
        "id_paciente" : dados.get("id_paciente"),
        "id_medico" : dados.get("id_medico"),
        "data" : dados.get("data"),
        "prescricao" : dados.get("prescricao")
    })
    if(resposta_laudo):
        retorno = f"Laudo documentado com sucesso"
        auditoria = retorno
        return True, retorno, auditoria
    else:
        retorno = f"Erro ao documentar laudo"
        auditoria = retorno
        return False, retorno, auditoria
    
def cadastrar_exame(dados):
    resposta_exame = exame.insert_one({
        "id_paciente" : dados.get("id_paciente"),
        "tipo_exame" : dados.get("tipo_exame"),
        "data" : dados.get("data"),
        "resultado" : dados.get("resultado"),
        "percentual_aceitacao" : dados.get("percentual_aceitacao") # Quão aceitável foi o exame para a saúde do paciente (métrica fictícia)
    })
    if(resposta_exame):
        retorno = f"Exame registrado com sucesso"
        auditoria = retorno
        return True, retorno, auditoria
    else:
        retorno = f"Erro ao registrar exame"
        auditoria = retorno
        return False, retorno, auditoria
    
def consultar_laudo(dados):
    resposta_laudo = laudo.find_one({
        "id_paciente" : dados.get("id_paciente"),
        "data" : dados.get("data")
    })
    if(resposta_laudo):
        retorno = {
            'id_paciente' : resposta_laudo['id_paciente'],
            'id_medico' : resposta_laudo['id_medico'],
            'data' : resposta_laudo['data'],
            'prescricao' : resposta_laudo['prescricao']
        }
        auditoria = f"Laudo consultado com sucesso"
        return True, retorno, auditoria
    else:
        retorno = f"Erro ao consultar laudo"
        auditoria = retorno
        return False, retorno, auditoria

def consultar_exame(dados):
    resposta_exame = exame.find_one({
        "id_paciente" : dados.get("id_paciente"),
        "data" : dados.get("data")
    })
    if(resposta_exame):
        retorno = retorno = {
            'id_paciente' : resposta_exame['id_paciente'],
            'tipo_exame' : resposta_exame['tipo_exame'],
            'data' : resposta_exame['data'],
            'resultado' : resposta_exame['resultado'],
            'percentual_aceitacao' : resposta_exame['percentual_aceitacao']
        }
        auditoria = f"Exame consultado com sucesso"
        return True, retorno, auditoria
    else:
        retorno = f"Erro ao consultar exame"
        auditoria = retorno
        return False, retorno, auditoria