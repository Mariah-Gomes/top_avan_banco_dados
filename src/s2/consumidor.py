# PASSO 1: Importar bibliotecas
import pika
import json
from src.s2.rdb import verificar_dado_medico, inserir_dado_medico, remover_dado_medico, consultar_dado_medico

# PASSO 2: Criar função de callback para processar as mensagens
def callback(ch, method, properties, body):
    try:
        mensagem = json.loads(body)
        dados = mensagem.get('dados')
        fila = method.routing_key
        
        # Imprime o que foi recebido
        print(" [x] Recebido")
        #print(f" [x] Recebido: função={fila}, dados={dados}")

        if fila == 'verificar_medico':
            sucesso, mensagem_resultado = verificar_dado_medico(dados)
            resultado = {'resultado': sucesso, 'mensagem': mensagem_resultado}
        elif fila == 'adicionar_medico':
            sucesso, mensagem_resultado = inserir_dado_medico(dados)
            resultado = {'resultado': sucesso, 'mensagem': mensagem_resultado}
        elif fila == 'remover_medico':
            sucesso, mensagem_resultado = remover_dado_medico(dados)
            resultado = {'resultado': sucesso, 'mensagem': mensagem_resultado}
        elif fila == 'consultar_medico':
            sucesso, mensagem_resultado = consultar_dado_medico(dados)
            resultado = {'resultado': sucesso, 'mensagem': mensagem_resultado}
        else:
            print('Nenhuma operação encontrada')
            
        if properties.reply_to:
            ch.basic_publish(
                exchange = '',
                routing_key = properties.reply_to,
                body = json.dumps(resultado),
                properties = pika.BasicProperties(
                    correlation_id=properties.correlation_id
                    )
                )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Erro", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# PASSO 3: Configurar a conexão com o RabbitMQ
rabbitmq_host = "localhost"
credenciais = pika.PlainCredentials('guest', 'guest')
paramentros_conexao = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credenciais)

# PASSO 4: Abrir o canal e a conexão para a comunicação com RabbitMQ
conexao = pika.BlockingConnection(paramentros_conexao)
canal = conexao.channel()

# PASSO 5: Declarar a fila de onde o consumidor vai escutar
lista_filas = ['verificar_medico', 'adicionar_medico', 'remover_medico', 'consultar_medico']
# PASSO 6: Consumir as mensagens da fila
for fila in lista_filas:
    canal.queue_declare(queue=fila, durable=True)
    canal.basic_consume(queue=fila, on_message_callback=callback)

# PASSO 7: Iniciar o consumo de mensagens
print()
print("......")
print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
print("......")
print()
canal.start_consuming()