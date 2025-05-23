import pika
import json

def enviar_mensagem(nome_fila, dados, reply_to=None, correlation_id=None):
    rabbitmq_host = "localhost"
    credenciais = pika.PlainCredentials('guest', 'guest')
    parametros_conexao = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credenciais)

    conexao = None

    try:
        conexao = pika.BlockingConnection(parametros_conexao)
        canal = conexao.channel()

        canal.queue_declare(queue=nome_fila, durable=True)

        mensagem = {'dados': dados}

        propriedades_mensagem = pika.BasicProperties(
            delivery_mode=2,
            reply_to=reply_to,
            correlation_id=correlation_id
        )

        canal.basic_publish(
            exchange='',
            routing_key=nome_fila,
            body=json.dumps(mensagem),
            properties=propriedades_mensagem
        )

        print()
        print("......")
        print(" [x] Mensagem enviada para a fila!")
        print("......")
        print()

    except Exception as e:
        print('Erro ao inserir a mensagem', e)

    finally:
        if conexao and conexao.is_open:
            conexao.close()
