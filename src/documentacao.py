def menu_documentacao():
    print("Menu Documentação: ")
    print("---------------")
    print("1. Documentar laudo")
    print("2. Buscar laudo")
    print("3. Registrar exame")
    print("4. Buscar exame")
    print("5. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        print("Documentar laudo")
    elif opcao == 2:
        print("Buscar laudo")
    elif opcao == 3:
        print("Registrar exame")
    elif opcao == 4:
        print("Buscar exame")
    elif opcao == 5:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()