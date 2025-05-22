from src.s1.medico import adicionar_medico, remover_medico, consultar_medico, listar_medicos
from src.s1.paciente import adicionar_paciente, remover_paciente, consultar_paciente, listar_pacientes
from src.s1.medico import adicionar_disponibilidade, editar_disponibilidade

def menu_dados():
    print("Menu Dados: ")
    print("---------------")
    print("1. Médico")
    print("2. Paciente")
    print("3. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        menu_quem("Médico")
    elif opcao == 2:
        menu_quem("Paciente")
    elif opcao == 3:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()

def menu_quem(quem):
    print(f'Menu {quem}:')
    print("---------------")
    print("1. Cadastrar")
    print("2. Remover")
    print("3. Horários")
    print("4. Consultar")
    print("5. Listar")
    print("6. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        cadastrar(quem)
    elif opcao == 2:
        remover(quem)
    elif opcao == 3:
        editar(quem)
    elif opcao == 4:
        consultar(quem)
    elif opcao == 5:
        listar(quem)
    elif opcao == 6:
        print("Tchau!")
    else:
        print("Opção inválida!")

def cadastrar(quem):
    if quem == "Médico":
        adicionar_medico()
    elif quem == "Paciente":
        adicionar_paciente()
        
def remover(quem):
    if quem == "Médico":
        remover_medico()
    elif quem == "Paciente":
        remover_paciente()
        
def editar(quem):
   if quem == "Médico":
        print("3.1. Adicionar Disponibilidade")
        print("3.2. Editar Disponibilidade")
        opcaoDentro = input("Digite a opção: ")
        if opcaoDentro == '3.1':
            adicionar_disponibilidade()
        elif opcaoDentro == '3.2':
            editar_disponibilidade()
        else:
            print("Essa opção não se encontra")
   elif quem == "Paciente":
        print("Essa opção só está disponível para médico")
        
def consultar(quem):
    if quem == "Médico":
        consultar_medico()
    elif quem == "Paciente":
        consultar_paciente()
        
def listar(quem):
    if quem == "Médico":
        listar_medicos()
    elif quem == "Paciente":
        listar_pacientes()