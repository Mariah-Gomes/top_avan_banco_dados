from src.s2.cassandraConnection import create_cassandra_session
from src.s2.createTableCassandra import create_table_agenda_medico
from cassandra.query import dict_factory
from datetime import datetime, date, timedelta
from uuid import uuid4
from src.s2.connection import supabase  # conexão com o Supabase
import datetime as dt  # para não confundir com 'from datetime import'

# Criar sessão e garantir que a tabela exista
session = create_cassandra_session()
create_table_agenda_medico(session)


def dias_disponiveis(session, medico_id):
    try:
        query = """
        SELECT data_hora, status FROM agenda_medico 
        WHERE medico_id = %s AND status = 'livre';
        """
        resultados = session.execute(query, (medico_id,))
        dias = set()
        for row in resultados:
            dias.add(row.data_hora.date())
        dias_ordenados = sorted(list(dias))
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