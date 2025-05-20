# PASSO 1: Imports
import pika
import json

def enviar_mensagem(nome_fila, dados, reply_to=None, correlation_id=None):
    # PASSO 2: Configurar conexão
    rabbitmq_host = "localhost"
    credenciais = pika.PlainCredentials('guest', 'guest')
    paramentros_conexao = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credenciais)
    
    # PASSO 3: Abrir Conexão
    try:
        conexao = pika.BlockingConnection(paramentros_conexao)
        canal = conexao.channel()
        
        # PASSO 4: Declarar fila
        canal.queue_declare(queue=nome_fila, durable=True)
        
        # PASSO 5: Montar corpo da mensagem
        mensagem = {'dados': dados}

        # PASSO 6: Configurar propriedades da mensagem
        propriedades_mensagem = pika.BasicProperties(
            delivery_mode=2,
            reply_to=reply_to,
            correlation_id=correlation_id)

        # PASSO 7: Publicar mensagem na fila
        canal.basic_publish(
            exchange='',
            routing_key=nome_fila,
            body=json.dumps(mensagem),
            properties=propriedades_mensagem    
        )

        # PASSO 8: Imprimir mensagem de sucesso
        print()
        print("......")
        print(" [x] Mensagem enviada para a fila!")
        print("......")
        print()
        
    except Exception as e:
        print('Erro ao inserir a mensagem', e)

    # PASSO 9: Fechar a conexão com segurança
    finally:
        if conexao and conexao.is_open:
            conexao.close()