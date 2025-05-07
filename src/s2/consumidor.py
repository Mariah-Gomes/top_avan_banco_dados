import pika
import json
from src.s2.rdb import inserir_dado_medico, verificar_dado_medico

def callback(ch, method, properties, body):
    try:
        mensagem = json.loads(body)
        funcao = mensagem.get('funcao')
        dados = mensagem.get('dados')

        print(f" [x] Recebido: função={funcao}, dados={dados}")

        resultado = None

        if funcao == 'adicionar_medico':
            resultado = inserir_dado_medico(dados)
        elif funcao == 'verificar_medico':
            resultado = verificar_dado_medico(dados)
        else:
            print(f" [!] Função desconhecida: {funcao}")

        if properties.reply_to:
            resposta = {'funcao': funcao, 'resultado': resultado}
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=json.dumps(resposta),
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Erro ao processar mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

rabbitmq_host = "localhost"
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='medico', durable=True)
channel.basic_consume(queue='medico', on_message_callback=callback)

print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
channel.start_consuming()
