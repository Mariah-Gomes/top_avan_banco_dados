# ===== IMPORTS =====
import datetime as dt
from datetime import date, timedelta
from uuid import uuid4
#from cassandra.query import dict_factory

from src.s2.cassandraConnection import create_cassandra_session
from src.s2.createTableCassandra import create_table_agenda_medico
from src.s2.connection import supabase

# ===== SESSÃO CASSANDRA =====
session = create_cassandra_session()
# session.row_factory = dict_factory  # se quiser retornar dicts
create_table_agenda_medico(session)  # Criação da tabela logo após a conexão

# ===== TRADUÇÃO DOS DIAS DA SEMANA =====
dias_semana_traducao = {
    "Monday": "segunda",
    "Tuesday": "terça",
    "Wednesday": "quarta",
    "Thursday": "quinta",
    "Friday": "sexta",
    "Saturday": "sábado",
    "Sunday": "domingo"
}

# ===== FUNÇÕES AUXILIARES =====
def str_hora_para_datetime(hora_str):
    try:
        return dt.datetime.strptime(hora_str, '%H:%M:%S').time()
    except ValueError:
        return dt.datetime.strptime(hora_str, '%H:%M').time()

def gera_slots_30min(inicio: dt.time, fim: dt.time):
    slots = []
    current = dt.datetime.combine(date.today(), inicio)
    end = dt.datetime.combine(date.today(), fim)
    while current < end:
        slots.append(current.time())
        current += dt.timedelta(minutes=30)
    return slots

# ===== FUNÇÃO PRINCIPAL: GERAÇÃO DE AGENDA =====
def gerar_agenda_automaticamente(medico_id, disponibilidades=None):
    # Se não passou as disponibilidades, busca no supabase
    if disponibilidades is None:
        resposta = supabase.table('disponibilidade_fixa').select('*').eq('id_medico', medico_id).execute()
        disponibilidades = resposta.data

    if not disponibilidades:
        print("Nenhuma disponibilidade encontrada para o médico.")
        return

    hoje = date.today()

    for dia in (hoje + timedelta(n) for n in range(31)):
        dia_semana_en = dia.strftime('%A')
        dia_semana_pt = dias_semana_traducao[dia_semana_en]

        for d in disponibilidades:
            if d['dia_semana'].lower() == dia_semana_pt:
                inicio = str_hora_para_datetime(d['hora_inicio'])
                fim = str_hora_para_datetime(d['hora_fim'])
                slots = gera_slots_30min(inicio, fim)

                for slot in slots:
                    data_hora = dt.datetime.combine(dia, slot)
                    consulta_id = uuid4()
                    status = 'livre'

                    result = session.execute("""
                        SELECT * FROM consultas.agenda_medico
                        WHERE medico_id = %s AND data_hora = %s
                    """, (medico_id, data_hora))

                    #print(f"[DEBUG] Verificando se já existe consulta: {data_hora}")

                    if result.one() is None:
                        print(f"[INSERINDO] Médico {medico_id}, Data: {data_hora}")
                        session.execute("""
                            INSERT INTO consultas.agenda_medico (
                                medico_id, data_hora, consulta_id, paciente_id, status
                            ) VALUES (%s, %s, %s, %s, %s)
                        """, (medico_id, data_hora, consulta_id, 0, status))

    print("Agenda automática gerada com sucesso!")

# ===== FUNÇÃO: CONSULTAR DIAS DISPONÍVEIS =====
def dias_disponiveis(medico_id):
    try:
        query = """
        SELECT data_hora, status FROM agenda_medico 
        WHERE medico_id = %s AND status = 'livre';
        """
        resultados = session.execute(query, (medico_id,))
        dias = {row.data_hora.date() for row in resultados}
        dias_ordenados = sorted(dias)

        if not dias_ordenados:
            mensagem = f"Médico {medico_id} não possui dias disponíveis para consulta."
        else:
            mensagem = f"Consulta de dias disponíveis para médico {medico_id} realizada com sucesso."

        resposta = {
            "medico_id": medico_id,
            "dias_disponiveis": dias_ordenados,
            "mensagem": mensagem
        }
        return True, resposta, mensagem

    except Exception as e:
        mensagem_erro = f"Erro na consulta de dias disponíveis para médico {medico_id}: {str(e)}"
        resposta = {
            "medico_id": medico_id,
            "dias_disponiveis": []
        }
        return False, resposta, mensagem_erro