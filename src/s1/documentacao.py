import tkinter as tk
from tkinter import filedialog, messagebox
import re
import fitz  # PyMuPDF

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
        registrar_exame()
    elif opcao == 4:
        print("Buscar exame")
    elif opcao == 5:
        print("Tchau!")
    else:
        print("Opção inválida!")
    print()

def registrar_exame():
    exames = []

    cpf = input("Digite o CPF do paciente: ")
    data = input("Digite a data dos exames (formato: DD/MM/AAAA): ")
    quant_exames = int(input("Digite quantos exames foram realizados: "))

    for i in range(quant_exames):
        print(f"\n--- Exame {i+1} ---")
        tipo = input("Digite o tipo do exame: ")
        resultado = input("Digite o resultado do exame: ")

        exame = {
            'tipo': tipo,
            'resultado': resultado,
        }
        exames.append(exame)

    # Prepara os dados finais
    dados_para_envio = {
        'cpf_paciente': cpf,
        'exames': exames,
        'data': data  # mesma data para todos
    }

    # Envia via mensageria
    resposta = enviar_mensagem_aguardando('registrar_exames', dados_para_envio)
    print(resposta['mensagem'])
