import psycopg2

try:
    connection = psycopg2.connect(
        user="usuario_api",
        password="senha123",
        host="192.168.0.201",
        port="5432",
        database="biblioteca"
    )
    print("Conexão realizada com sucesso!")
    connection.close()
except Exception as error:
    print(f"Erro ao conectar: {error}")



