# ===== IMPORTS =====
import datetime as dt
from datetime import date, timedelta
from uuid import uuid4
from cassandra.query import SimpleStatement
from datetime import datetime
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
        SELECT data_hora FROM agenda_medico 
        WHERE medico_id = %s AND status = 'livre' ALLOW FILTERING;
        """
        resultados = session.execute(query, (medico_id,))
        resultados = list(resultados)  # força avaliação para debug
        lista_temporaria = [row.data_hora.strftime("%d/%m/%Y %H:%M") for row in resultados]
        horarios = sorted(lista_temporaria)

        if not horarios:
            mensagem = f"Médico {medico_id} não possui horários disponíveis para consulta."
            sucesso = True
        else:
            mensagem = f"Consulta de horários disponíveis para médico {medico_id} realizada com sucesso."
            sucesso = True

        resposta = {
            "horarios_disponiveis": horarios,
            "mensagem": mensagem
        }

        auditoria = mensagem
        return sucesso, resposta, auditoria

    except Exception as e:
        print(f"DEBUG - Erro na consulta de horários disponíveis para médico {medico_id}: {e}")
        mensagem_erro = f"Erro na consulta de horários disponíveis para médico {medico_id}: {str(e)}"
        resposta = {
            "medico_id": medico_id,
            "horarios_disponiveis": []
        }
        return False, resposta, mensagem_erro

def buscar_consulta_id(medico_id, data_hora):
    try:
        query = """
        SELECT consulta_id FROM agenda_medico 
        WHERE medico_id = %s AND data_hora = %s ALLOW FILTERING;
        """
        statement = SimpleStatement(query)
        resultado = session.execute(statement, (medico_id, data_hora))
        row = resultado.one()

        if row:
            return row.consulta_id
        else:
            print(f"Nenhuma consulta encontrada para médico {medico_id} no horário {data_hora}")
            return None
    except Exception as e:
        print(f"Erro ao buscar consulta_id: {e}")
        return None


def agendamento_consulta(dados):
    try:
        medico_id = dados.get("id_medico")
        data_hora_str = dados.get("dia_hora")
        paciente_id = dados.get("id_paciente")

        if not medico_id or not data_hora_str or not paciente_id:
            mensagem = "Erro: dados incompletos. Verifique id_medico, dia_hora e id_paciente."
            auditoria = mensagem
            return False, mensagem, auditoria

        try:
            data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
        except ValueError:
            mensagem = f"Formato de data inválido: {data_hora_str}. Use 'dd/mm/aaaa hh:mm'."
            auditoria = mensagem
            return False, mensagem, auditoria

        consulta_id = buscar_consulta_id(medico_id, data_hora)

        if not consulta_id:
            mensagem = f"Nenhuma consulta encontrada para médico {medico_id} nesse horário."
            auditoria = mensagem
            return False, mensagem, auditoria

        update_query = """
        UPDATE agenda_medico 
        SET status = 'agendado', paciente_id = %s 
        WHERE medico_id = %s AND data_hora = %s AND consulta_id = %s;
        """
        session.execute(update_query, (paciente_id, medico_id, data_hora, consulta_id))

        mensagem = f"Consulta agendada com sucesso para médico {medico_id} em {data_hora.strftime('%d/%m/%Y %H:%M')}."
        auditoria = mensagem
        return True, mensagem, auditoria

    except Exception as e:
        mensagem_erro = f"Erro ao agendar consulta: {e}"
        auditoria = mensagem_erro
        return False, mensagem_erro, auditoria

def cancelamento_consulta(dados):
    try:
        medico_id = dados.get("id_medico")
        data_hora_str = dados.get("dia_hora")
        paciente_id = dados.get("id_paciente")

        if not medico_id or not data_hora_str or not paciente_id:
            mensagem = "Erro: dados incompletos. Verifique id_medico, dia_hora e id_paciente."
            auditoria = mensagem
            return False, mensagem, auditoria

        try:
            data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
        except ValueError:
            mensagem = f"Formato de data inválido: {data_hora_str}. Use 'dd/mm/aaaa hh:mm'."
            auditoria = mensagem
            return False, mensagem, auditoria

        consulta_id = buscar_consulta_id(medico_id, data_hora)

        if not consulta_id:
            mensagem = f"Nenhuma consulta encontrada para médico {medico_id} nesse horário."
            auditoria = mensagem
            return False, mensagem, auditoria

        update_query = """
        UPDATE agenda_medico 
        SET status = 'livre', paciente_id = %s 
        WHERE medico_id = %s AND data_hora = %s AND consulta_id = %s;
        """
        session.execute(update_query, (0, medico_id, data_hora, consulta_id))

        mensagem = f"Consulta cancelada com sucesso para médico {medico_id} em {data_hora.strftime('%d/%m/%Y %H:%M')}."
        auditoria = mensagem
        return True, mensagem, auditoria

    except Exception as e:
        mensagem_erro = f"Erro ao cancelar consulta: {e}"
        auditoria = mensagem_erro
        return False, mensagem_erro, auditoria