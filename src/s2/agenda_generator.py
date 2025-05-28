import datetime as dt
from datetime import date, timedelta
from uuid import uuid4
from .rdb import supabase
from .cassandra import session

def str_hora_para_datetime(hora_str):
    return dt.datetime.strptime(hora_str, '%H:%M').time()

def gera_slots_30min(inicio: dt.time, fim: dt.time):
    slots = []
    current = dt.datetime.combine(date.today(), inicio)
    end = dt.datetime.combine(date.today(), fim)
    while current < end:
        slots.append(current.time())
        current += dt.timedelta(minutes=30)
    return slots

def gerar_agenda_automaticamente(medico_id):
    resposta = supabase.table('disponibilidade_fixa').select('*').eq('id_medico', medico_id).execute()
    disponiveis = resposta.data

    if not disponiveis:
        print("Nenhuma disponibilidade encontrada para o médico.")
        return

    hoje = date.today()

    for dia in (hoje + timedelta(n) for n in range(31)):
        dia_semana_nome = dia.strftime('%A')  # ex: 'Monday'

        for d in disponiveis:
            if d['dia_semana'] == dia_semana_nome:
                inicio = str_hora_para_datetime(d['hora_inicio'])
                fim = str_hora_para_datetime(d['hora_fim'])
                slots = gera_slots_30min(inicio, fim)

                for slot in slots:
                    data_hora = dt.datetime.combine(dia, slot)
                    consulta_id = uuid4()
                    status = 'livre'

                    # Verifica se o slot já existe
                    result = session.execute("""
                        SELECT * FROM consultas.agenda_medico
                        WHERE medico_id = %s AND data_hora = %s
                    """, (medico_id, data_hora))

                    if result.one() is None:
                        session.execute("""
                            INSERT INTO consultas.agenda_medico (
                                medico_id, data_hora, consulta_id, paciente_id, status
                            ) VALUES (%s, %s, %s, %s, %s)
                        """, (medico_id, data_hora, consulta_id, None, status))

    print("Agenda automática gerada com sucesso!")