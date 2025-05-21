from src.utils import enviar_mensagem_aguardando  # Importa a função de envio de mensagem do módulo produtor

def menu_consulta():
    print("Menu Consulta: ")
    print("---------------")
    print("1. Agendar")
    print("2. Buscar")
    print("3. Cancelar")
    print("4. Histórico")
    print("5. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        agendar()
    elif opcao == 2:
        buscar()
    elif opcao == 3:
        cancelar()
    elif opcao == 4:
        historico()
    elif opcao == 5:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()

def consultar_id():
    nome_medico = input("Digite o nome do médico: ") 
    cpf = input("Digite o CPF do paciente: ")

    dados = {'nome_medico': nome_medico, 'cpf': cpf}
    resposta = enviar_mensagem_aguardando("buscar_ids", dados)

    if not resposta.get("resultado"):
        print("❌ Erro:", resposta.get("mensagem"))
        return None

    ids = resposta.get("mensagem")

    print(ids.get("mensagem"))
    print("Médico ID:", ids.get("id_medico"))
    print("Paciente ID:", ids.get("id_paciente"))

    return ids  # Retorna o dicionário com os IDs

#def verificao_disponibilidade():
 #   resultado = enviar_mensagem_aguardando('verificar_disponibilidade', crm)  # Envia o CRM para verificar no backend


def agendar():
    ids = consultar_id()
    if not ids:
        return  # Se não conseguiu buscar os IDs, encerra aqui

    id_medico = ids.get("id_medico")
    id_paciente = ids.get("id_paciente")
    if id_medico == None:
        print("Médico não cadastrado no sistema")
        return
    elif id_paciente == None:
        print("Paciente não cadastrado no sistema")
        return
    elif id_paciente == None and id_medico == None:
        print("Paciente e médicos não cadastrado no sistema")
        return
    
    # Verifica disponibilidade com Cassandra
    resposta_dias = enviar_mensagem_aguardando("dias_disponiveis", {"id_medico": id_medico})



    



    
def buscar():
    print('Busca a consulta do paciente')
    
def cancelar():
    print('Muda o status de cancelada')
    
def historico():
    print()