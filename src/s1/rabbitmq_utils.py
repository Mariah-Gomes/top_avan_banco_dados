import pika  # Biblioteca para trabalhar com RabbitMQ
import uuid  # Para gerar identificadores únicos
import json  # Para converter dados entre Python e JSON
from src.s1.produtor import enviar_mensagem  # Importa a função de envio de mensagem do módulo produtor

# Função que envia uma mensagem para o RabbitMQ e espera uma resposta antes de continuar
def enviar_mensagem_aguardando(nome_funcao, dados):
    # Estabelece conexão com o RabbitMQ em localhost
    conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conexao.channel()  # Abre um canal de comunicação

    # Cria uma fila temporária exclusiva para receber a resposta
    result = canal.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue  # Guarda o nome da fila temporária

    # Gera um ID único para rastrear a mensagem e preparar o dicionário de resposta
    correlation_id = str(uuid.uuid4())
    resposta = {'received': False, 'body': None}

    # Define a função callback para processar a resposta recebida
    def on_response(ch, method, props, body):
        # Verifica se a resposta recebida tem o mesmo correlation_id da mensagem enviada
        if props.correlation_id == correlation_id:
            resposta['received'] = True  # Marca que recebeu resposta
            resposta['body'] = json.loads(body)  # Converte a resposta JSON para dicionário Python
            ch.stop_consuming()  # Interrompe a espera por mensagens

    # Configura o consumidor para ouvir a fila de callback e usar a função on_response
    canal.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True  # Mensagem será automaticamente confirmada como processada
    )

    # Envia a mensagem para o RabbitMQ informando para onde deve ser enviada a resposta
    enviar_mensagem(nome_funcao, dados, reply_to=callback_queue, correlation_id=correlation_id)

    print()
    print('******')
    print(' [*] Aguardando resposta...')  # Mensagem informando que está esperando a resposta
    print('******')
    print()
    canal.start_consuming()  # Começa a consumir as mensagens da fila (bloqueia aqui até receber resposta)
    conexao.close()  # Fecha a conexão após o consumo

    return resposta['body']  # Retorna o corpo da resposta recebida