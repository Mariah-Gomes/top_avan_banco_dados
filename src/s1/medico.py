from src.s1.rabbitmq_utils import enviar_mensagem_aguardando

# Função para verificar se um CRM já está cadastrado
def verificacao_medico(crm):
    resultado = enviar_mensagem_aguardando('verificar_medico', crm)  # Envia o CRM para verificar no backend
    if resultado and resultado['resultado']:
        #print("Atenção: CRM já cadastrado!")  # Exibe aviso se já existir
        return True  # Indica que está cadastrado
    else:
        #print("CRM disponível para cadastro.")  # Exibe confirmação se não existir
        return False  # Indica que não está cadastrado

# Função para adicionar um médico no sistema
def adicionar_medico():
    # Solicita informações ao usuário
    nome_medico = input("Digite o nome do médico: ")
    crm = input("Digite o CRM do médico: ")

    # Verifica se o CRM já está cadastrado
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível adicionar médico com CRM já cadastrado.")
        return  # Interrompe a função se já estiver cadastrado
    print()
    print('------')
    print('[x] Resposta recebida... CRM não cadastrado, seguindo a operação')
    print('------')
    print()
    # Solicita a especialização do médico
    especializacao = input("Digite a especialização do médico: ")

    # Prepara os dados do médico para envio
    dados = {'nome': nome_medico, 'crm': crm, 'especializacao': especializacao}
    resultado = enviar_mensagem_aguardando('adicionar_medico', dados)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])

def remover_medico():
    crm = input("Digite o CRM do médico: ")
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível remover um médico que não está no sistema.")
        return 
    
    print()
    print('------')
    print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    print('------')
    print()
    
    resultado = enviar_mensagem_aguardando('remover_medico', crm)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])

# Função Editar Comentada para dúvidas futuras   
#def editar_medico():
    #crm = input("Digite o CRM do médico: ")
    #ja_cadastrado = verificacao_medico(crm)
    #if not ja_cadastrado:
    #    print("Operação cancelada: não é possível remover um médico que não está no sistema.")
    #    return
    
    #print()
    #print('------')
    #print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    #print('------')
    #print()
    
    #resultado = enviar_mensagem_aguardando('editar_medico', crm)  # Envia os dados para adicionar no backend
    #print(resultado['mensagem'])
    
def consultar_medico():
    crm = input("Digite o CRM do médico: ")
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível consultar um médico que não está no sistema.")
        return
    
    print()
    print('------')
    print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    print('------')
    print()
    
    resultado = enviar_mensagem_aguardando('consultar_medico', crm)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])
    
def listar_medicos():
    resultado = enviar_mensagem_aguardando('listar_medicos', None)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])