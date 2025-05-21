from src.s1.rabbitmq_utils import enviar_mensagem_aguardando

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

#def verificao_disponibilidade():
 #   resultado = enviar_mensagem_aguardando('verificar_disponibilidade', crm)  # Envia o CRM para verificar no backend

def agendar():
    nome_medico = input("Digite o nome do médico: ") 
    nome_paciente = input("Digite o nome do paciente: ")
    cpf = input("Digite o CPF do paciente: ")

    dados = {'nome_medico': nome_medico, 'nome_paciente': nome_paciente, 'cpf': cpf}
    
    # Envia para mensageria e aguarda retorno dos IDs
    ids = enviar_mensagem_aguardando("buscar_ids", dados)
    print(ids)

    print('Retorna com possíveis dias e horários')
    
    #dia = 
    #hora = 
    
def buscar():
    print('Busca a consulta do paciente')
    
def cancelar():
    print('Muda o status de cancelada')
    
def historico():
    print()