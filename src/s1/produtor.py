import pika
import json

def enviar_mensagem(nome_funcao, dados):
    rabbitmq_host = "localhost"
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
    connection = None

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declara a fila única
        channel.queue_declare(queue='medico', durable=True)

        # Monta o payload com função + dados
        mensagem = {
            'funcao': nome_funcao,
            'dados': dados
        }

        # Envia mensagem para a fila 'medico'
        channel.basic_publish(
            exchange='',
            routing_key='medico',
            body=json.dumps(mensagem),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f" [x] Mensagem enviada para a fila! ({nome_funcao})")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()
