from mongoConnection import get_mongo_client

client = get_mongo_client()
db = client['OperacaoBanco']
colecao = db['Clientes']
