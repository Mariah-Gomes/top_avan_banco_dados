from src.s1.dados import menu_dados
from src.s1.consulta import menu_consulta
from src.s1.documentacao import menu_documentacao
from src.s1.acompanhamento import acompanhamento

# Loop principal:
print("Bem-vindo(a) ao Sistema AgendaMed!!!")
while(True):
    print("Menu de Acesso: ")
    print("---------------")
    print("1. Dados")
    print("2. Consulta")
    print("3. Documentação")
    print("4. Acompanhamento")
    print("5. Sair")
    print("---------------")
    opcao = int(input("Digite uma opção -> "))
    if opcao == 1:
        print()
        menu_dados()
    elif opcao == 2:
        print()
        menu_consulta()
    elif opcao == 3:
        print()
        menu_documentacao()
    elif opcao == 4:
        print()
        acompanhamento()
    elif opcao == 5:
        print("Tchau!")
        break
    else:
        print("Opção inválida!")