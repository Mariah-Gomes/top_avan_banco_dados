import pika
import uuid
import json
from src.s1.produtor import enviar_mensagem

def enviar_mensagem_aguardando(nome_funcao, dados):
    conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conexao.channel()

    result = canal.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    correlation_id = str(uuid.uuid4())
    resposta = {'received': False, 'body': None}

    def on_response(ch, method, props, body):
        if props.correlation_id == correlation_id:
            resposta['received'] = True
            resposta['body'] = json.loads(body)

    canal.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    enviar_mensagem(nome_funcao, dados, reply_to=callback_queue, correlation_id=correlation_id)

    print('\n[*] Aguardando resposta do consumidor...')

    # ✅ Espera até que a resposta seja recebida
    while not resposta['received']:
        conexao.process_data_events(time_limit=0.5)

    # ✅ Só fecha depois de garantir o recebimento
    try:
        canal.queue_delete(queue=callback_queue)
    except Exception as e:
        print(f"Erro ao deletar fila temporária: {e}")

    conexao.close()

    return resposta['body']
