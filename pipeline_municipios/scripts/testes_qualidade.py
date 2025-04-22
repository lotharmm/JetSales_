import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "municipios_db",
    "user": "airflow",
    "password": "airflow"
}

def executar_teste(cursor, descricao, query):
    cursor.execute(query)
    resultado = cursor.fetchone()[0]
    status = "✅ OK" if resultado == 0 else f"❌ FALHA ({resultado})"
    print(f"{descricao}: {status}")

def testar_qualidade():
    print("Executando testes de qualidade...\n")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    testes = [
        {
            "descricao": "1. Municípios com código IBGE nulo (tabela populacao)",
            "query": "SELECT COUNT(*) FROM populacao WHERE codigo_municipio IS NULL"
        },
        {
            "descricao": "2. Duplicatas de código IBGE na tabela populacao",
            "query": """
                SELECT COUNT(*) FROM (
                    SELECT codigo_municipio FROM populacao GROUP BY codigo_municipio HAVING COUNT(*) > 1
                ) AS duplicados
            """
        },
        {
            "descricao": "3. População negativa",
            "query": "SELECT COUNT(*) FROM populacao WHERE populacao_estimada < 0"
        },
        {
            "descricao": "4. Notas ENEM maiores que 1000",
            "query": "SELECT COUNT(*) FROM enem WHERE media_matematica > 1000 OR media_linguagens > 1000"
        },
        {
            "descricao": "5. Notas ENEM negativas",
            "query": "SELECT COUNT(*) FROM enem WHERE media_matematica < 0 OR media_linguagens < 0"
        },
        {
            "descricao": "6. Códigos de município no ENEM que não existem na tabela populacao",
            "query": """
                SELECT COUNT(*) FROM enem e
                LEFT JOIN populacao p ON e.codigo_municipio = p.codigo_municipio
                WHERE p.codigo_municipio IS NULL
            """
        }
    ]

    for teste in testes:
        executar_teste(cursor, teste["descricao"], teste["query"])

    cursor.close()
    conn.close()
    print("\nTestes finalizados.")

if __name__ == "__main__":
    testar_qualidade()
