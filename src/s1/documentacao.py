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
        print("Buscar laudo")
    elif opcao == 3:
        print("Registrar exame")
    elif opcao == 4:
        print("Buscar exame")
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