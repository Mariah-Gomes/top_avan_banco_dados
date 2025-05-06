# s2/consumidor.py 
import pika
import json
from src.s2.rdb import inserir_dado_medico
from src.s2.mongo import inserir_dado_mongo  # Caso tenha MongoDB
from src.s2.cassandra import inserir_dado_cassandra  # Caso tenha Cassandra

def callback(ch, method, properties, body):
    # Converte a mensagem de volta para um dicionário
    dados = json.loads(body.decode())
    print(f" [x] Mensagem recebida: {dados}")

    # Pega a routing_key da mensagem (nome da fila)
    routing_key = method.routing_key
    print(f" [x] Mensagem recebida na fila: {routing_key}")

    # Decide qual função chamar com base na routing_key
    if routing_key == 'medico':
        sucesso = inserir_dado_medico(dados)
    elif routing_key == 'documento':
        sucesso = inserir_dado_mongo(dados)
    elif routing_key == 'disponibilidade':
        sucesso = inserir_dado_cassandra(dados)
    else:
        sucesso = False
        print("Erro: routing_key desconhecida.")

    # Feedback de sucesso ou falha
    if sucesso:
        print("Operação realizada com sucesso no banco de dados.")
    else:
        print("Erro ao realizar a operação no banco de dados.")

# Estabelece a conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',  # Ou 'rabbitmq' se você estiver usando Docker Compose, conforme o nome do serviço
    credentials=pika.PlainCredentials('guest', 'guest')  # Credenciais do RabbitMQ
))
channel = connection.channel()

# Declara as filas que quer escutar
filas = ['medico', 'documento', 'disponibilidade']

for fila in filas:
    channel.queue_declare(queue=fila)
    channel.basic_consume(queue=fila, on_message_callback=callback, auto_ack=True)

print(' [*] Esperando mensagens. Pressione CTRL+C para sair.')
channel.start_consuming()
