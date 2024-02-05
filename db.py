import psycopg2
from sqlalchemy import create_engine


# Substitua essas informações pelos detalhes do seu banco de dados
dbname = "postgres"
user = "postgres"
password = 'password'
host = "localhost"
port = "5432"

# Construa a string de conexão
conn_string = f"dbname={dbname} user={user} password={password} host={host} port={port}"

# Crie uma conexão usando SQLAlchemy (pode ser necessário instalar com 'pip install sqlalchemy')
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

# Conecte ao banco de dados
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print('Conectado ao banco de dados Localhost!')