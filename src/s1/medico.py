from src.utils import enviar_mensagem_aguardando  # Importa a função de envio de mensagem do módulo produtor
from datetime import datetime

dias_validos = ['segunda', 'terca', 'terça', 'quarta', 'quinta', 'sexta']

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

def validar_dados_disponibilidade():
    while True:
        dia = input("Digite o dia da semana (segunda a sexta): ").strip().lower()
        if dia not in dias_validos:
            print("Dia inválido. Só é permitido cadastrar de segunda a sexta-feira.\n")
            continue

        hora_inicio = input("Digite o horário de início (HH:MM): ").strip()
        hora_fim = input("Digite o horário de fim (HH:MM): ").strip()

        try:
            hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M")
            hora_fim_dt = datetime.strptime(hora_fim, "%H:%M")
        except ValueError:
            print("Formato de hora inválido. Use o formato HH:MM, exemplo: 09:00.\n")
            continue

        if not (8 <= hora_inicio_dt.hour < 18) or not (9 <= hora_fim_dt.hour <= 18):
            print("Horários devem estar entre 08:00 e 18:00.\n")
            continue

        if hora_inicio_dt >= hora_fim_dt:
            print("O horário de início deve ser antes do horário de fim.\n")
            continue

        # Se passou por todas as validações:
        print("Dados validados com sucesso.\n")
        return dia, hora_inicio, hora_fim

def adicionar_disponibilidade():
    crm = input("Digite o CRM do médico: ")
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível adicionar a disponibilidade de um médico que não está no sistema.")
        return
    
    print()
    print('------')
    print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    print('------')
    print()
    
    id_medico = enviar_mensagem_aguardando('buscar_idMedico', crm)
    id_medico2 = id_medico['mensagem']['id_medico']
    
    dia_semana, hora_inicio, hora_fim = validar_dados_disponibilidade()

    dados = {
        'id_medico': id_medico2,
        'dia_semana': dia_semana,
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim
    }

    resultado = enviar_mensagem_aguardando('adicionar_disponibilidade', dados)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])
    
def editar_disponibilidade():
    crm = input("Digite o CRM do médico: ")
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível editar a disponibilidade de um médico que não está no sistema.")
        return
    id_medico = enviar_mensagem_aguardando('buscar_ids', crm)
    print()
    print('------')
    print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    print('------')
    print()
    
    dia_semana = input('Digite o dia da semana: ')
    hora_inicio = input('Digte o horário de início do expediente: ')
    hora_fim = input('Digite o horário de fim do expediente: ')
    
    dados = {
        'id_medico': id_medico,
        'dia_semana': dia_semana,
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim
    }

    resultado = enviar_mensagem_aguardando('editar_disponibilidade', dados)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])

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