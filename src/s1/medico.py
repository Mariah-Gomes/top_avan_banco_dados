import pika
import uuid
import json
from src.s1.produtor import enviar_mensagem

def verificacao_medico(crm):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    correlation_id = str(uuid.uuid4())
    resposta = {'received': False, 'body': None}

    def on_response(ch, method, props, body):
        if props.correlation_id == correlation_id:
            resposta['received'] = True
            resposta['body'] = json.loads(body)
            ch.stop_consuming()

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    enviar_mensagem('verificar_medico', crm, reply_to=callback_queue, correlation_id=correlation_id)

    print(' [*] Aguardando resposta...')
    channel.start_consuming()
    connection.close()

    resultado = resposta['body']
    if resultado and resultado['resultado']:
        print("⚠️ Atenção: CRM já cadastrado!")
        return True
    else:
        print("✅ CRM disponível para cadastro.")
        return False

def adicionar_medico():
    nome_medico = input("Digite o nome do médico: ")
    crm = input("Digite o CRM do médico: ")

    ja_cadastrado = verificacao_medico(crm)
    if ja_cadastrado:
        print("🚫 Operação cancelada: não é possível adicionar médico com CRM já cadastrado.")
        return

    especializacao = input("Digite a especialização do médico: ")

    dados = {'nome': nome_medico, 'crm': crm, 'especializacao': especializacao}
    enviar_mensagem('adicionar_medico', dados)
    print("✅ Médico enviado para a fila!")

def remover_medico():
    crm = input("Digite o CRM do médico: ")
    dados = {'crm': crm}
    enviar_mensagem('remover_medico', dados)
    print("Médico removido (caso tenha sido encontrado)!")

def editar_medico():
    crm = input("Digite o CRM do médico: ")
    dados = {'crm': crm}
    enviar_mensagem('editar_medico', dados)
    print("Médico editado (caso tenha sido encontrado)!")

def consultar_medico():
    crm = input("Digite o CRM do médico: ")
    dados = {'crm': crm}
    enviar_mensagem('consultar_medico', dados)
    print("Médico consultado (caso tenha sido encontrado)!")
