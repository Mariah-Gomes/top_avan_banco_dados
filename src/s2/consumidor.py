import pika
import json
from src.s2.rdb import verificar_dado_medico, inserir_dado_medico, remover_dado_medico, consultar_dado_medico, listar_dado_medico
from src.s2.rdb import verificar_dado_paciente, inserir_dado_paciente, remover_dado_paciente, consultar_dado_paciente, listar_dado_paciente
from src.s2.rdb import buscar_ids_paciente_medico
from src.s2.rdb import adicionar_disponibilidade_medico, editar_disponibilidade_medico, buscar_id_medico, verificar_disponibilidade_medico
from src.s2.cassandra import dias_disponiveis
from src.s1.auditoria import salvar_mensagem, criar_tabela

def salvar_resultado_operacao(fila, sucesso, mensagem_resultado):
    status_str = "SUCESSO" if sucesso else "ERRO"
    salvar_mensagem(fila, mensagem_resultado, status_str)

def callback(ch, method, properties, body):
    try:
        print(" [x] Mensagem recebida", flush=True)
        mensagem = json.loads(body.decode())
        dados = mensagem.get('dados')
        fila = method.routing_key

        criar_tabela()

        if fila == 'verificar_medico':
            sucesso, mensagem_retorno, mensagem_a = verificar_dado_medico(dados)
            if not sucesso:
                sucesso = True
        elif fila == 'adicionar_medico':
            sucesso, mensagem_retorno, mensagem_a = inserir_dado_medico(dados)
        elif fila == 'remover_medico':
            sucesso, mensagem_retorno, mensagem_a = remover_dado_medico(dados)
        elif fila == 'adicionar_disponibilidade':
            sucesso, mensagem_retorno, mensagem_a = adicionar_disponibilidade_medico(dados)
        elif fila == 'editar_disponibilidade':
            sucesso, mensagem_retorno, mensagem_a = editar_disponibilidade_medico(dados)
        elif fila == 'buscar_idMedico':
            sucesso, mensagem_retorno, mensagem_a = buscar_id_medico(dados)
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
        elif fila == 'buscar_ids':
            sucesso, mensagem_retorno, mensagem_a = buscar_ids_paciente_medico(dados)
        elif fila == 'agendamento_consulta':
            sucesso, mensagem_retorno, mensagem_a = dias_disponiveis(dados)
        elif fila == 'verificar_disponibilidade':
            sucesso, mensagem_retorno, mensagem_a = verificar_disponibilidade_medico(dados)
        else:
            print("Operação desconhecida", flush=True)
            sucesso = False
            mensagem_retorno = "Operação desconhecida"
            mensagem_a = "Operação não reconhecida no consumidor."

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
            print(" [x] Resposta enviada para o produtor", flush=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("!!! Erro no callback:", e, flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

rabbitmq_host = "localhost"
credenciais = pika.PlainCredentials('guest', 'guest')
paramentros_conexao = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credenciais)

conexao = pika.BlockingConnection(paramentros_conexao)
canal = conexao.channel()

lista_filas = [
    'verificar_medico', 'adicionar_medico', 'remover_medico', 'consultar_medico', 'listar_medicos',
    'verificar_paciente', 'adicionar_paciente', 'remover_paciente', 'consultar_paciente', 'listar_paciente',
    'buscar_ids', 'agendamento_consulta', 'adicionar_disponibilidade', 'editar_disponibilidade', 'buscar_idMedico',
    'verificar_disponibilidade'
]

for fila in lista_filas:
    canal.queue_declare(queue=fila, durable=True)
    canal.basic_consume(queue=fila, on_message_callback=callback)

print("", flush=True)
print("......", flush=True)
print(' [*] Aguardando mensagens. Para sair pressione CTRL+C', flush=True)
print("......", flush=True)
print("", flush=True)

canal.start_consuming()
