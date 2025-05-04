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
        print(f'Cadastrar {quem}')
    elif opcao == 2:
        print(f'Remover {quem}')
    elif opcao == 3:
        print(f'Editar {quem}')
    elif opcao == 4:
        print(f'Consultar {quem}')
    elif opcao == 5:
        print(f'Listar {quem}')
    elif opcao == 6:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()