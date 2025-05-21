from src.s2.cassandraConnection import create_cassandra_session
from src.s2.createTableCassandra import create_table_agenda_medico

session = create_cassandra_session()
create_table_agenda_medico(session)
