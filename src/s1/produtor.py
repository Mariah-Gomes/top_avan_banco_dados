import pika  # Biblioteca para comunicação com RabbitMQ
import json  # Biblioteca para converter objetos Python em JSON

def enviar_mensagem(nome_funcao, dados, reply_to=None, correlation_id=None):
    # Define o endereço do servidor RabbitMQ (localhost significa máquina local)
    rabbitmq_host = "localhost"
    
    # Cria as credenciais padrão para autenticação (usuário guest, senha guest)
    credentials = pika.PlainCredentials('guest', 'guest')
    
    # Define os parâmetros de conexão (host, porta, virtual host, credenciais)
    parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
    
    # Inicializa a variável da conexão (será usada no try e fechada no finally)
    connection = None

    try:
        # Abre uma conexão bloqueante com o RabbitMQ
        connection = pika.BlockingConnection(parameters)
        
        # Cria um canal de comunicação dentro da conexão
        channel = connection.channel()
        
        # Declara (ou garante que existe) a fila chamada 'medico'
        # O parâmetro durable=True faz a fila sobreviver a reinícios do servidor
        channel.queue_declare(queue='medico', durable=True)

        # Monta o corpo da mensagem como um dicionário
        mensagem = {
            'funcao': nome_funcao,  # Nome da função que o consumidor deve executar
            'dados': dados           # Dados que serão enviados para essa função
        }

        # Define as propriedades da mensagem
        props = pika.BasicProperties(
            delivery_mode=2,          # Torna a mensagem persistente (salva em disco)
            reply_to=reply_to,        # Nome da fila para onde a resposta deve ser enviada (se necessário)
            correlation_id=correlation_id  # ID único para correlacionar requisição e resposta
        )

        # Publica (envia) a mensagem para a fila 'medico'
        channel.basic_publish(
            exchange='',              # Exchange padrão (sem troca personalizada)
            routing_key='medico',     # Nome da fila de destino
            body=json.dumps(mensagem),  # Converte o dicionário mensagem para JSON
            properties=props           # Adiciona as propriedades configuradas acima
        )

        # Exibe no terminal que a mensagem foi enviada com sucesso
        print("[x] Mensagem enviada para a fila!")
    
    except Exception as e:
        # Se ocorrer algum erro durante o envio, exibe a mensagem de erro
        print(f"Erro ao enviar mensagem: {e}")
    
    finally:
        # No final (com ou sem erro), verifica se a conexão está aberta e fecha ela
        if connection and connection.is_open:
            connection.close()
