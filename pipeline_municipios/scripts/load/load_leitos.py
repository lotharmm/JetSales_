import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "municipios_db",
    "user": "airflow",
    "password": "airflow"
}

def criar_e_popular_leitos():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 1. Criar a tabela de leitos
    print("Criando tabela 'leitos'...")
    cursor.execute("""
        DROP TABLE IF EXISTS leitos CASCADE;

        CREATE TABLE leitos (
            codigo_municipio VARCHAR(20) PRIMARY KEY,
            ano INT,
            leitos_totais INT,
            leitos_uti INT,
            leitos_clinicos INT,
            FOREIGN KEY (codigo_municipio) REFERENCES populacao(codigo_municipio)
        );
    """)

    # 2. Inserir dados fictícios
    print("Populando tabela com dados fictícios...")
    cursor.execute("""
        INSERT INTO leitos (
            codigo_municipio,
            ano,
            leitos_totais,
            leitos_uti,
            leitos_clinicos
        )
        SELECT 
            p.codigo_municipio,
            2024,
            FLOOR(RANDOM() * 291 + 10)::INT AS leitos_totais,         -- 10 a 300
            FLOOR(RANDOM() * 101)::INT AS leitos_uti,                 -- 0 a 100
            FLOOR(RANDOM() * 191 + 10)::INT AS leitos_clinicos        -- 10 a 200
        FROM 
            populacao p;
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabela 'leitos' criada e populada com sucesso.")

if __name__ == "__main__":
    criar_e_popular_leitos()
