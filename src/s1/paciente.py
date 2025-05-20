from datetime import datetime
from src.s1.rabbitmq_utils import enviar_mensagem_aguardando

# Função para verificar se um CRM já está cadastrado
def verificacao_paciente(cpf):
    resultado = enviar_mensagem_aguardando('verificar_paciente', cpf)  # Envia o CRM para verificar no backend
    if resultado and resultado['resultado']:
        #print("Atenção: CRM já cadastrado!")  # Exibe aviso se já existir
        return True  # Indica que está cadastrado
    else:
        #print("CRM disponível para cadastro.")  # Exibe confirmação se não existir
        return False  # Indica que não está cadastrado

# Função para adicionar um médico no sistema
def adicionar_paciente():
    # Solicita informações ao usuário
    nome_paciente = input("Digite o nome do paciente: ")
    cpf = input("Digite o CPF do paciente: ")

    # Verifica se o CPF já está cadastrado
    ja_cadastrado = verificacao_paciente(cpf)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível adicionar médico com CRM já cadastrado.")
        return  # Interrompe a função se já estiver cadastrado
    print()
    print('------')
    print('[x] Resposta recebida... CPF não cadastrado, seguindo a operação')
    print('------')
    print()
    # Solicita a especialização do paciente
    data_nascimento = input("Digite a de nascimento do paciente: ")
    sexo = input("Digite o sexo do paciente: ")

    # ✅ Converte a data para o formato ISO aceito pelo banco
    try:
        data_formatada = datetime.strptime(data_nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Formato de data inválido. Use o formato DD/MM/AAAA.")
        return

    # Prepara os dados do médico para envio
    dados = {'nome': nome_paciente, 'cpf': cpf, 'data_de_nascimento': data_formatada, 'sexo': sexo}
    resultado = enviar_mensagem_aguardando('adicionar_paciente', dados)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])
    
def remover_paciente():
    cpf = input("Digite o CPF do paciente: ")
    ja_cadastrado = verificacao_paciente(cpf)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível remover um médico que não está no sistema.")
        return 
    
    print()
    print('------')
    print('[x] Resposta recebida... CPF Cadastrado, seguindo a operação')
    print('------')
    print()
    
    resultado = enviar_mensagem_aguardando('remover_paciente', cpf)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])
    
def consultar_paciente():
    cpf = input("Digite o CPF do paciente: ")
    ja_cadastrado = verificacao_paciente(cpf)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível consultar um paciente que não está no sistema.")
        return
    
    print()
    print('------')
    print('[x] Resposta recebida... CPF Cadastrado, seguindo a operação')
    print('------')
    print()
    
    resultado = enviar_mensagem_aguardando('consultar_paciente', cpf)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])
    
def listar_pacientes():
    resultado = enviar_mensagem_aguardando('listar_paciente', None)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])