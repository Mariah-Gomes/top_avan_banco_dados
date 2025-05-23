import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

# Caminho correto até o .env (na raiz do projeto)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.getenv('ASTRA_CLIENT_ID')
CLIENT_SECRET = os.getenv('ASTRA_CLIENT_SECRET')
KEYSPACE = os.getenv('ASTRA_KEYSPACE')
SECURE_CONNECT_BUNDLE = os.getenv('ASTRA_SECURE_CONNECT_BUNDLE')

def create_cassandra_session():
    # AQUI: aponta para o .zip na raiz do projeto
    SECURE_CONNECT_BUNDLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', SECURE_CONNECT_BUNDLE))

    cloud_config = {
        'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
    }

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    session.set_keyspace(KEYSPACE)
    print("Conectado no AstraDB Cassandra!")
    return session
