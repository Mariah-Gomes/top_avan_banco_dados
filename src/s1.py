# Loop principal:
print()
print("Bem-vindo(a) ao Sistema AgendaMed!!!")
while(True):
    print()
    print("Menu de Acesso: ")
    print("---------------")
    print("1. Dados")
    print("2. Consulta")
    print("3. Documentação")
    print("4. Acompanhamento")
    print("5. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção: "))
    if opcao == 1:
        print("Dados")
    elif opcao == 2:
        print("Consulta")
    elif opcao == 3:
        print("Documentação")
    elif opcao == 4:
        print("Acompanhamento")
    elif opcao == 5:
        print("Tchau!")
        break
    else:
        print("Opção inválida!")