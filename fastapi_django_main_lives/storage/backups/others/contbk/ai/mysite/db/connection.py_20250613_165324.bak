import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname="neondb",
        user=os.getenv("postgre_user"),
        password=os.getenv("postgre_pass"),
        host=os.getenv("postgre_host"),
        port=5432,
        sslmode="require"
    )
    return conn