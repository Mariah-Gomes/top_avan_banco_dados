from src.s1.medico import adicionar_medico, remover_medico

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
    print("3. Editar")
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
        consultar()
    elif opcao == 5:
        listar()
    elif opcao == 6:
        print("Tchau!")
    else:
        print("Opção inválida!")

def cadastrar(quem):
    if quem == "Médico":
        adicionar_medico()
    elif quem == "Paciente":
        print(f'Cadastrar {quem}')
        
def remover(quem):
    if quem == "Médico":
        remover_medico()
    elif quem == "Paciente":
        print(f'Remover {quem}')
        
def editar(quem):
    if quem == "Médico":
        print(f'Editar {quem}')
    elif quem == "Paciente":
        print(f'Editar {quem}')
        
def consultar(quem):
    if quem == "Médico":
        print(f'Consultar {quem}')
    elif quem == "Paciente":
        print(f'Consultar {quem}')
        
def listar(quem):
    if quem == "Médico":
        print(f'Listar {quem}')
    elif quem == "Paciente":
        print(f'Listar {quem}')