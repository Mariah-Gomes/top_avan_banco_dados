def adicionar_medico():
    nome_medico = input("Digite o nome do médico: ")
    crm = input("Digite o CRM do médico: ")
    especializacao = input("Digite a especialização do médico: ")
    dados = {
        'nome': nome_medico,
        'crm': crm,
        'especialidade': especializacao
    }
    # CHAMA A FUNÇÃO PARA INSERIR NO BANCO DE DADOS
    #inserir_dado('medico', dados)
    #sucesso = rdb.inserir_medico(dados)

    #if sucesso:
    #    print("Médico cadastrado com sucesso!")
    #else:
    #    print("Ocorreu um erro ao cadastrar o médico. Tente novamente!")

def remover_medico():
    crm = input("Digite o CRM do médico: ")
    #remover_dado('medico', crm)
    #sucesso = rdb.remover_medico(crm)

    #if sucesso:
    #    print("Médico removido com sucesso!")
    #else:
    #    print("Ocorreu um erro ao remover o médico. Tente novamente!")
    
def editar_medico():
    crm = input("Digite o CRM do médico: ")
    #editar_dado('medico', crm)
    #sucesso = rdb.editar_medico(crm)

    #if sucesso:
    #    print("Informações do médico editadas com sucesso!")
    #else:
    #    print("Ocorreu um erro ao editar informações do médico. Tente novamente!")
    
def consultar_medico():
    crm = input("Digite o nome do médico: ")
    #consultar_dado('medico', nome_medico)
    #medico = rdb.consultar_medico(nome)

    #if medico:
    #    print("Médico encontrado:")
    #    print(f"Nome: {medico['nome']}")
    #    print(f"CRM: {medico['crm']}")
    #    print(f"Especialidade: {medico['especialidade']}")
    #else:
    #    print("Nenhum médico encontrado com esse nome.")

def listar():
    print()