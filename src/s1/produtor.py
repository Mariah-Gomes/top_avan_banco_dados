import pika
import json

def enviar_mensagem(nome_funcao, dados, reply_to=None, correlation_id=None):
    rabbitmq_host = "localhost"
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
    connection = None

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='medico', durable=True)

        mensagem = {
            'funcao': nome_funcao,
            'dados': dados
        }

        props = pika.BasicProperties(
            delivery_mode=2,
            reply_to=reply_to,
            correlation_id=correlation_id
        )

        channel.basic_publish(
            exchange='',
            routing_key='medico',
            body=json.dumps(mensagem),
            properties=props
        )

        print(f" [x] Mensagem enviada para a fila! ({nome_funcao})")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()
