from src.s2.mongoConnection import get_mongo_db

db = get_mongo_db()

# Coleções
laudo = db['laudo']
exame = db['prescricao']

# Inserir em laudo
def inserir_exame(id_paciente, tipo_exame, data, resultado):
    exame.insert_one({
        "id_paciente": id_paciente,
        "tipo_exame": tipo_exame,
        "data": data,
        "resultado": resultado
    })

# Inserir em prescricao
def inserir_lado(id_paciente, id_medico, data, prescricao_texto):
    laudo.insert_one({
        "id_paciente": id_paciente,
        "id_medico": id_medico,
        "data": data,
        "prescricao": prescricao_texto
    })
