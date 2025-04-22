import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "municipios_db",
    "user": "airflow",
    "password": "airflow"
}

def criar_e_popular_enem():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 1. Criar a tabela enem
    print("Criando tabela 'enem'...")
    cursor.execute("""
        DROP TABLE IF EXISTS enem CASCADE;

        CREATE TABLE enem (
            id SERIAL PRIMARY KEY,
            codigo_municipio VARCHAR(20) REFERENCES populacao(codigo_municipio),
            ano INTEGER NOT NULL,
            media_matematica NUMERIC(5,2),
            media_linguagens NUMERIC(5,2),
            percentual_participacao NUMERIC(5,2)
        );
    """)

    # 2. Inserir dados fictícios
    print("Populando tabela com dados fictícios...")
    cursor.execute("""
        INSERT INTO enem (codigo_municipio, ano, media_matematica, media_linguagens, percentual_participacao)
        SELECT 
            p.codigo_municipio,
            2024,
            ROUND((RANDOM() * 1000)::NUMERIC, 2) AS media_matematica,
            ROUND((RANDOM() * 1000)::NUMERIC, 2) AS media_linguagens,
            ROUND((RANDOM() * 100)::NUMERIC, 2) AS percentual_participacao
        FROM populacao p;
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabela 'enem' criada e populada com sucesso.")

if __name__ == "__main__":
    criar_e_popular_enem()
