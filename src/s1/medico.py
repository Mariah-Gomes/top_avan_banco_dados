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

# Função para verificar se um CRM já está cadastrado
def verificacao_medico(crm):
    resultado = enviar_mensagem_aguardando('verificar_medico', crm)  # Envia o CRM para verificar no backend
    if resultado and resultado['resultado']:
        #print("Atenção: CRM já cadastrado!")  # Exibe aviso se já existir
        return True  # Indica que está cadastrado
    else:
        #print("CRM disponível para cadastro.")  # Exibe confirmação se não existir
        return False  # Indica que não está cadastrado

# Função para adicionar um médico no sistema
def adicionar_medico():
    # Solicita informações ao usuário
    nome_medico = input("Digite o nome do médico: ")
    crm = input("Digite o CRM do médico: ")

    # Verifica se o CRM já está cadastrado
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível adicionar médico com CRM já cadastrado.")
        return  # Interrompe a função se já estiver cadastrado
    print()
    print('------')
    print('[x] Resposta recebida... CRM não cadastrado, seguindo a operação')
    print('------')
    print()
    # Solicita a especialização do médico
    especializacao = input("Digite a especialização do médico: ")

    # Prepara os dados do médico para envio
    dados = {'nome': nome_medico, 'crm': crm, 'especializacao': especializacao}
    resultado = enviar_mensagem_aguardando('adicionar_medico', dados)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])

def remover_medico():
    crm = input("Digite o CRM do médico: ")
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível remover um médico que não está no sistema.")
        return 
    
    print()
    print('------')
    print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    print('------')
    print()
    
    resultado = enviar_mensagem_aguardando('remover_medico', crm)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])

# Função Editar Comentada para dúvidas futuras   
#def editar_medico():
    #crm = input("Digite o CRM do médico: ")
    #ja_cadastrado = verificacao_medico(crm)
    #if not ja_cadastrado:
    #    print("Operação cancelada: não é possível remover um médico que não está no sistema.")
    #    return
    
    #print()
    #print('------')
    #print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    #print('------')
    #print()
    
    #resultado = enviar_mensagem_aguardando('editar_medico', crm)  # Envia os dados para adicionar no backend
    #print(resultado['mensagem'])
    
def consultar_medico():
    crm = input("Digite o CRM do médico: ")
    ja_cadastrado = verificacao_medico(crm)
    if not ja_cadastrado:
        print("Operação cancelada: não é possível consultar um médico que não está no sistema.")
        return
    
    print()
    print('------')
    print('[x] Resposta recebida... CRM Cadastrado, seguindo a operação')
    print('------')
    print()
    
    resultado = enviar_mensagem_aguardando('consultar_medico', crm)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])
    
def listar_medicos():
    resultado = enviar_mensagem_aguardando('listar_medicos', None)  # Envia os dados para adicionar no backend
    print(resultado['mensagem'])