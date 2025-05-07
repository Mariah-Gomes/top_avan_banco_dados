from src.s1.produtor import enviar_mensagem

def adicionar_medico():
    nome_medico = input("Digite o nome do médico: ")
    crm = input("Digite o CRM do médico: ")
    especializacao = input("Digite a especialização do médico: ")

    dados = {
        'nome': nome_medico,
        'crm': crm,
        'especializacao': especializacao
    }

    # Agora passa o nome da função
    enviar_mensagem('adicionar_medico', dados)

    print("Médico enviado para a fila!")


# Função para remover médico
def remover_medico():
    crm = input("Digite o CRM do médico: ")
    funcao_nome = "remover_medico"  # Nome da função chamada
    dados = {'crm': crm}
    
    enviar_mensagem(funcao_nome, dados)  # Passa a função e os dados
    print("Médico removido (caso tenha sido encontrado)!")

# Função para editar médico
def editar_medico():
    crm = input("Digite o CRM do médico: ")
    funcao_nome = "editar_medico"  # Nome da função chamada
    dados = {'crm': crm}
    
    enviar_mensagem(funcao_nome, dados)  # Passa a função e os dados
    print("Médico editado (caso tenha sido encontrado)!")

# Função para consultar médico
def consultar_medico():
    crm = input("Digite o CRM do médico: ")
    funcao_nome = "consultar_medico"  # Nome da função chamada
    dados = {'crm': crm}
    
    enviar_mensagem(funcao_nome, dados)  # Passa a função e os dados
    print("Médico consultado (caso tenha sido encontrado)!")
