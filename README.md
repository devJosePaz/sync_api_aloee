endpoints/ → cada arquivo lida com um endpoint da API (produtos, modelos, etc).

db/ → funções de conexão e upserts/deletes.

utils/ → funções auxiliares:

api_client.py → funções genéricas de requisição à API (get_token, get_data_from_api)

logger.py → função que escreve .txt detalhando o que foi processado

main.py → importa endpoints, processa os dados e chama funções de banco.