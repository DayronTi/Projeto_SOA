import psycopg2

# Teste de conexão com o banco de dados PostgreSQL
# Este script verifica se a API consegue se conectar ao SGBD

try:
    # Estabelece conexão com o banco PostgreSQL
    connection = psycopg2.connect(
        user="usuario_api",       # Usuário do banco
        password="senha123",      # Senha do usuário
        host="192.168.0.201",     # Endereço IP do servidor PostgreSQL
        port="5432",              # Porta padrão do PostgreSQL
        database="biblioteca"     # Nome do banco de dados
    )

    # Mensagem exibida quando a conexão é realizada com sucesso
    print("Conexão realizada com sucesso!")

    # Encerra a conexão após o teste
    connection.close()

except Exception as error:
    # Exibe detalhes do erro caso a conexão falhe
    print(f"Erro ao conectar: {error}")