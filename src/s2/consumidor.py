# PASSO 1: Importar bibliotecas
import pika
import json
from src.s2.rdb import verificar_dado_medico, inserir_dado_medico, remover_dado_medico, consultar_dado_medico, listar_dado_medico
from src.s2.rdb import verificar_dado_paciente, inserir_dado_paciente, remover_dado_paciente, consultar_dado_paciente, listar_dado_paciente
from src.s1.auditoria import salvar_mensagem, criar_tabela

# PASSO 2: Criar função de callback para processar as mensagens
# Função para salvar os resultados da operação no SQLite
def salvar_resultado_operacao(fila, sucesso, mensagem_resultado):
    status_str = "SUCESSO" if sucesso else "ERRO"
    salvar_mensagem(fila, mensagem_resultado, status_str)

# Função de callback refatorada
def callback(ch, method, properties, body):
    try:
        mensagem = json.loads(body)
        dados = mensagem.get('dados')
        fila = method.routing_key
        
        print(" [x] Recebido")

        criar_tabela()  # Garante que a tabela existe

        if fila == 'verificar_medico':
            sucesso, mensagem_retorno, mensagem_a = verificar_dado_medico(dados)
            if not sucesso:
                sucesso = True
                
        elif fila == 'adicionar_medico':
            sucesso, mensagem_retorno, mensagem_a = inserir_dado_medico(dados)

        elif fila == 'remover_medico':
            sucesso, mensagem_retorno, mensagem_a = remover_dado_medico(dados)

        elif fila == 'consultar_medico':
            sucesso, mensagem_retorno, mensagem_a = consultar_dado_medico(dados)
            
        elif fila == 'listar_medicos':
            sucesso, mensagem_retorno, mensagem_a = listar_dado_medico()
            
        elif fila == 'verificar_paciente':
            sucesso, mensagem_retorno, mensagem_a = verificar_dado_paciente(dados)
            if not sucesso:
                sucesso = True
                
        elif fila == 'adicionar_paciente':
            sucesso, mensagem_retorno, mensagem_a = inserir_dado_paciente(dados)
            
        elif fila == 'remover_paciente':
            sucesso, mensagem_retorno, mensagem_a = remover_dado_paciente(dados)
            
        elif fila == 'consultar_paciente':
            sucesso, mensagem_retorno, mensagem_a = consultar_dado_paciente(dados)
        
        elif fila == 'listar_paciente':
            sucesso, mensagem_retorno, mensagem_a = listar_dado_paciente()
        
        else:
            print("Operação Desconhecida")
            #sucesso = False
            #mensagem_resultado = "Operação desconhecida"

        # mensagem_produtor: é o que volta para o produtor
        # mensagem_auditoria: é o que será salvo no SQLite
        mensagem_produtor = mensagem_retorno
        mensagem_auditoria = f"Ação '{fila}' executada. Resultado: {mensagem_a}"

        salvar_resultado_operacao(fila, sucesso, mensagem_auditoria)
        resultado = {'resultado': sucesso, 'mensagem': mensagem_produtor}

        if properties.reply_to:
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                body=json.dumps(resultado),
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                )
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Erro:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# PASSO 3: Configurar a conexão com o RabbitMQ
rabbitmq_host = "localhost"
credenciais = pika.PlainCredentials('guest', 'guest')
paramentros_conexao = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credenciais)

# PASSO 4: Abrir o canal e a conexão para a comunicação com RabbitMQ
conexao = pika.BlockingConnection(paramentros_conexao)
canal = conexao.channel()

# PASSO 5: Declarar a fila de onde o consumidor vai escutar
lista_filas = ['verificar_medico', 'adicionar_medico', 'remover_medico', 'consultar_medico', 'listar_medicos', 
               'verificar_paciente', 'adicionar_paciente', 'remover_paciente', 'consultar_paciente', 'listar_paciente']
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