from src.utils import enviar_mensagem_aguardando

def acompanhamento():
    cpf = input("Digite o CPF do paciente: ")
    dados = {
        "cpf" : cpf,
    }
    resposta = enviar_mensagem_aguardando('buscar_idPaciente', dados)
    print(resposta.get("mensagem"))
    if resposta["resultado"]:
        id = resposta.get("mensagem")
        tipo_exame = input("Digite o tipo de exame: ")
        buscar = {
            "id_paciente" : id.get("id_paciente"),
            "tipo_exame" : tipo_exame
        }
        resposta_busca = enviar_mensagem_aguardando("acompanhamento", buscar)
        print(resposta_busca["mensagem"])
    else:
        return