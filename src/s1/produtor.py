import pika
import json

# Função para enviar a mensagem para o RabbitMQ
def enviar_mensagem(dados_medico):
    # Estabelece a conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    credentials=pika.PlainCredentials('guest', 'guest')
))
    channel = connection.channel()

    # Declara a fila
    channel.queue_declare(queue='medico')

    # Envia a mensagem (dados do médico) como JSON
    channel.basic_publish(exchange='',
                          routing_key='medico',
                          body=json.dumps(dados_medico))

    print(" [x] Mensagem enviada para a fila!")

    connection.close()
