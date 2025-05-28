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
        plt.style.use('ggplot')
        plt.figure(figsize=(12, 6))
        plt.plot(datas_formatadas, percentuais, marker='D', linestyle='-', color='#2a9d8f', linewidth=2, markersize=8, label='Aceitação')
        plt.title(f'Evolução do Percentual de Aceitação - Exame: {tipo_exame}', fontsize=16, fontweight='bold')
        plt.xlabel('Data', fontsize=14)
        plt.ylabel('Percentual (%)', fontsize=14)
        plt.ylim(0, 100)

        # Definindo manualmente os ticks do eixo X para mostrar exatamente as datas que você quer
        plt.xticks(datas_formatadas, [d.strftime('%Y-%m-%d') for d in datas_formatadas], rotation=45, fontsize=12)
        plt.yticks(fontsize=12)

        plt.grid(alpha=0.6)  # Grade um pouco transparente

        # Anotar os valores dos percentuais em cima dos pontos
        for x, y in zip(datas_formatadas, percentuais):
            plt.text(x, y + 2, f"{y:.1f}%", ha='center', fontsize=12, color='#264653')

        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.show()

    else:
        return