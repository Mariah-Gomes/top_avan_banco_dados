def menu_dados():
    print("Menu Dados: ")
    print("---------------")
    print("1. Médico")
    print("2. Paciente")
    print("3. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        print("Médico")
    elif opcao == 2:
        print("Paciente")
    elif opcao == 3:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()