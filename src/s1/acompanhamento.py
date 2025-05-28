from src.utils import enviar_mensagem_aguardando
import matplotlib.pyplot as plt
from datetime import datetime

def acompanhamento():
    cpf = input("Digite o CPF do paciente: ")
    dados = {
        "cpf" : cpf,
    }
    resposta = enviar_mensagem_aguardando('buscar_idPaciente', dados)
    print(resposta.get("mensagem"))
    if resposta["resultado"]:
        id = resposta.get("mensagem")
        tipo_exame = input("Digite o tipo de exame: ")
        buscar = {
            "id_paciente" : id.get("id_paciente"),
            "tipo_exame" : tipo_exame
        }
        resposta_busca = enviar_mensagem_aguardando("acompanhamento", buscar)
        print(resposta_busca["mensagem"])

        exames = resposta_busca["mensagem"]

        # Extrair e ordenar os dados
        datas = sorted(exames.keys())
        datas_formatadas = [datetime.strptime(d, "%Y-%m-%d") for d in datas]
        percentuais = [exames[d]['percentual_aceitacao'] for d in datas]

        # Gerar gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(datas_formatadas, percentuais, marker='o', linestyle='-', color='green')
        plt.title('Evolução do Percentual de Aceitação')
        plt.xlabel('Data')
        plt.ylabel('Percentual (%)')
        plt.ylim(0, 100)

        # Definindo manualmente os ticks do eixo X para mostrar exatamente as datas que você quer
        plt.xticks(datas_formatadas, [d.strftime('%Y-%m-%d') for d in datas_formatadas])

        plt.grid(True)
        plt.tight_layout()
        plt.show()

    else:
        return