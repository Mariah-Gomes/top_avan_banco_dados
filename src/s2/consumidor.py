import pika
import json
from src.s2.rdb import inserir_dado_medico  # 👉 importa seu arquivo rdb.py

# Função para processar mensagens
def callback(ch, method, properties, body):
    try:
        mensagem = json.loads(body)
        funcao = mensagem.get('funcao')
        dados = mensagem.get('dados')

        print(f" [x] Recebido: função={funcao}, dados={dados}")

        # Roteamento para funções no rdb.py
        if funcao == 'adicionar_medico':
            inserir_dado_medico(dados)
        elif funcao == 'remover_medico':
            print()
        elif funcao == 'editar_medico':
            print()
        elif funcao == 'consultar_medico':
            print()
        else:
            print(f" [!] Função desconhecida: {funcao}")

        # Confirma que a mensagem foi processada
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Erro ao processar mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# Configuração RabbitMQ
rabbitmq_host = "localhost"
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declara a fila
channel.queue_declare(queue='medico', durable=True)

# Consome mensagens
channel.basic_consume(queue='medico', on_message_callback=callback)

print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
channel.start_consuming()
