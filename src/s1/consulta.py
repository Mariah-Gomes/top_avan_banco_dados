def menu_consulta():
    print("Menu Consulta: ")
    print("---------------")
    print("1. Agendar")
    print("2. Buscar")
    print("3. Cancelar")
    print("4. Histórico")
    print("5. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        print("Agendar")
    elif opcao == 2:
        print("Buscar")
    elif opcao == 3:
        print("Cancelar")
    elif opcao == 4:
        print("Histórico")
    elif opcao == 5:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()

def agendar():
    print()