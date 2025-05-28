from src.utils import enviar_mensagem_aguardando

def menu_documentacao():
    print("Menu Documentação: ")
    print("---------------")
    print("1. Documentar laudo")
    print("2. Buscar laudo")
    print("3. Registrar exame")
    print("4. Buscar exame")
    print("5. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        documentar_laudo()
    elif opcao == 2:
        buscar_laudo()
    elif opcao == 3:
        registrar_exame()
    elif opcao == 4:
        buscar_exame()
    elif opcao == 5:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()

def documentar_laudo():
    cpf = input("Digite o CPF do paciente: ")
    crm = input("Digite o CRM do médico: ")
    dados = {
        "cpf" : cpf,
        "crm" : crm
    }
    resposta = enviar_mensagem_aguardando('buscar_ids', dados)
    print(resposta.get("mensagem"))
    if resposta["resultado"]:
        ids = resposta.get("mensagem")
        data = input("Digite a data do laudo (YYYY-MM-DD): ")
        prescricao = input("Digite a prescrição: ")
        documentar = {
            "id_paciente" : ids.get("id_paciente"),
            "id_medico" : ids.get("id_medico"),
            "data" : data,
            "prescricao" : prescricao
        }
        resposta_documentar = enviar_mensagem_aguardando("documentar_laudo", documentar)
        print(resposta_documentar["mensagem"])
    else:
        return
    
def buscar_laudo():
    cpf = input("Digite o CPF do paciente: ")
    dados = {
        "cpf" : cpf,
    }
    resposta = enviar_mensagem_aguardando('buscar_idPaciente', dados)
    print(resposta.get("mensagem"))
    if resposta["resultado"]:
        id = resposta.get("mensagem")
        data = input("Digite a data do laudo (YYYY-MM-DD): ")
        buscar = {
            "id_paciente" : id.get("id_paciente"),
            "data" : data,
        }
        resposta_busca = enviar_mensagem_aguardando("buscar_laudo", buscar)
        print(resposta_busca["mensagem"])
    else:
        return

def registrar_exame():
    cpf = input("Digite o CPF do paciente: ")
    dados = {
        "cpf" : cpf
    }
    resposta = enviar_mensagem_aguardando('buscar_idPaciente', dados)
    print(resposta.get("mensagem"))
    if resposta["resultado"]:
        id = resposta.get("mensagem")
        tipo_exame = input("Digite o tipo de exame feito: ")
        data = input("Digite a data do exame (YYYY-MM-DD): ")
        resultado = input("Digite o resultado: ")
        percentual_aceitacao = float(input("Digite o percentual de aceitação do exame: "))
        registrar = {
            "id_paciente" : id.get("id_paciente"),
            "tipo_exame" : tipo_exame,
            "data" : data,
            "resultado" : resultado,
            "percentual_aceitacao" : percentual_aceitacao
        }
        resposta_registrar = enviar_mensagem_aguardando("registrar_exame", registrar)
        print(resposta_registrar["mensagem"])
    else:
        return
    
def buscar_exame():
    cpf = input("Digite o CPF do paciente: ")
    dados = {
        "cpf" : cpf,
    }
    resposta = enviar_mensagem_aguardando('buscar_idPaciente', dados)
    print(resposta.get("mensagem"))
    if resposta["resultado"]:
        id = resposta.get("mensagem")
        data = input("Digite a data do exame (YYYY-MM-DD): ")
        buscar = {
            "id_paciente" : id.get("id_paciente"),
            "data" : data,
        }
        resposta_busca = enviar_mensagem_aguardando("buscar_exame", buscar)
        print(resposta_busca["mensagem"])
    else:
        return