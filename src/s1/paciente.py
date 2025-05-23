from datetime import datetime
from src.utils import enviar_mensagem_aguardando  # Usando função centralizada

def verificacao_paciente(cpf):
    resultado = enviar_mensagem_aguardando('verificar_paciente', cpf)
    return resultado and resultado['resultado']

def adicionar_paciente():
    nome_paciente = input("Digite o nome do paciente: ")
    cpf = input("Digite o CPF do paciente: ")

    if not verificacao_paciente(cpf):
        print("Operação cancelada: não é possível adicionar paciente com CPF já cadastrado.")
        return
    print("\n------\n[x] CPF não cadastrado, seguindo a operação\n------\n")

    data_nascimento = input("Digite a data de nascimento do paciente (DD/MM/AAAA): ")
    sexo = input("Digite o sexo do paciente: ")

    try:
        data_formatada = datetime.strptime(data_nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Formato de data inválido. Use o formato DD/MM/AAAA.")
        return

    dados = {'nome': nome_paciente, 'cpf': cpf, 'data_de_nascimento': data_formatada, 'sexo': sexo}
    resultado = enviar_mensagem_aguardando('adicionar_paciente', dados)
    print(resultado['mensagem'])

def remover_paciente():
    cpf = input("Digite o CPF do paciente: ")
    if not verificacao_paciente(cpf):
        print("Operação cancelada: paciente não está no sistema.")
        return

    print("\n------\n[x] CPF cadastrado, seguindo a operação\n------\n")
    resultado = enviar_mensagem_aguardando('remover_paciente', cpf)
    print(resultado['mensagem'])

def consultar_paciente():
    cpf = input("Digite o CPF do paciente: ")
    if not verificacao_paciente(cpf):
        print("Operação cancelada: paciente não está no sistema.")
        return

    print("\n------\n[x] CPF cadastrado, seguindo a operação\n------\n")
    resultado = enviar_mensagem_aguardando('consultar_paciente', cpf)
    print(resultado['mensagem'])

def listar_pacientes():
    resultado = enviar_mensagem_aguardando('listar_paciente', None)
    print(resultado['mensagem'])
