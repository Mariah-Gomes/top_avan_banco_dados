import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def create_table_agenda_medico(session):
    query = """
    CREATE TABLE IF NOT EXISTS agenda_medico (
        medico_id int,
        consulta_id uuid,
        paciente_id int,
        data_hora timestamp,
        status text,
        PRIMARY KEY (medico_id, data_hora, consulta_id)
    ) WITH CLUSTERING ORDER BY (data_hora ASC, consulta_id ASC);
    """
    session.execute(query)
    #print("Tabela 'agenda_medico' criada (se não existia).")