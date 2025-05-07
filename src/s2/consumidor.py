# Importação de bibliotecas necessárias
import pika  # Para comunicação com o RabbitMQ
import json  # Para converter dados em formato JSON
from src.s2.rdb import inserir_dado_medico, verificar_dado_medico, remover_dado_medico  # Funções para manipulação do banco de dados

# Função de callback que será chamada toda vez que uma mensagem for recebida na fila
def callback(ch, method, properties, body):
    try:
        # Converte a mensagem recebida (que está em formato JSON) para um dicionário Python
        mensagem = json.loads(body)
        
        # Extrai os dados da mensagem
        funcao = mensagem.get('funcao')  # A chave 'funcao' define qual ação o consumidor deve realizar
        dados = mensagem.get('dados')  # A chave 'dados' contém os dados a serem processados

        # Imprime o que foi recebido
        print(f" [x] Recebido")
        #print(f" [x] Recebido: função={funcao}, dados={dados}")

        # Variável para armazenar o resultado da operação
        resultado = None

        # Verifica qual função foi solicitada pela mensagem e executa a operação correspondente
        if funcao == 'adicionar_medico':
            # Chama a função para inserir os dados do médico no banco de dados
            sucesso, mensagem_resultado = inserir_dado_medico(dados)
            resultado = {'resultado': sucesso, 'mensagem': mensagem_resultado}
            
        elif funcao == 'remover_medico':
            # Chama a função para inserir os dados do médico no banco de dados
            sucesso, mensagem_resultado = remover_dado_medico(dados)
            resultado = {'resultado': sucesso, 'mensagem': mensagem_resultado}
        
        elif funcao == 'verificar_medico':
            # Chama a função para verificar se o médico já existe no banco de dados
            existe = verificar_dado_medico(dados)
            resultado = {'resultado': existe, 'mensagem': 'Verificação concluída'}
        else:
            # Caso a função não seja reconhecida
            resultado = {'resultado': False, 'mensagem': f'Função desconhecida: {funcao}'}

        # Se a mensagem original pediu uma resposta (indicado pela propriedade 'reply_to')
        if properties.reply_to:
            # Envia a resposta de volta para a fila de resposta especificada
            ch.basic_publish(
                exchange='',  # Não estamos usando um exchange, apenas a fila direta
                routing_key=properties.reply_to,  # Fila de resposta
                body=json.dumps(resultado),  # A resposta em formato JSON
                properties=pika.BasicProperties(  # Define as propriedades da mensagem de resposta
                    correlation_id=properties.correlation_id  # Correlation ID para rastrear a resposta
                )
            )

        # Confirma que a mensagem foi processada com sucesso
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        # Se ocorrer algum erro durante o processamento, exibe a mensagem de erro
        print(f" [!] Erro ao processar mensagem: {e}")
        # Se ocorreu um erro, a mensagem é negada e não é reencaminhada para outra fila
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


# Configuração da conexão com o RabbitMQ
rabbitmq_host = "localhost"  # Define o host do RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')  # Credenciais para autenticação no RabbitMQ
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)  # Parâmetros de conexão

# Estabelece a conexão com o RabbitMQ
connection = pika.BlockingConnection(parameters)
# Cria um canal de comunicação
channel = connection.channel()

# Declara a fila 'medico', garantindo que ela exista
channel.queue_declare(queue='medico', durable=True)  # 'durable=True' garante que a fila persista mesmo após reiniciar o RabbitMQ

# Diz ao canal que o callback acima será executado quando uma mensagem for recebida na fila 'medico'
channel.basic_consume(queue='medico', on_message_callback=callback)

# Inicia o consumo da fila e aguarda novas mensagens
print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
channel.start_consuming()
