import pandas as pd
import psycopg2

ARQUIVO_XLS = "data/raw/populacao_2024.xls"
ABA = "MUNICÍPIOS"

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "municipios_db",
    "user": "airflow",
    "password": "airflow"
}

def carregar_populacao():
    print("Lendo o arquivo Excel...")
    df = pd.read_excel(ARQUIVO_XLS, sheet_name=ABA, skiprows=2)

    # Renomeia colunas
    df.columns = ['uf', 'cod_uf', 'cod_munic', 'nome_municipio', 'populacao_estimada']

    # Remove linhas com dados ausentes
    df = df.dropna(subset=['cod_uf', 'cod_munic', 'nome_municipio', 'populacao_estimada'])

    # Formata código do município (somente cod_munic com 5 dígitos)
    df['codigo_municipio'] = df['cod_munic'].astype(str).str.zfill(5)

    # Limpa população (remove ponto e converte pra inteiro)
    df['populacao_estimada'] = df['populacao_estimada'].astype(str).str.replace(".", "", regex=False).astype(int)

    # Seleciona colunas finais
    df = df[['codigo_municipio', 'nome_municipio', 'populacao_estimada']]

    # Conecta ao banco e insere os dados
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO populacao (codigo_municipio, nome_municipio, populacao_estimada)
            VALUES (%s, %s, %s)
            ON CONFLICT (codigo_municipio) DO NOTHING
        """, (row['codigo_municipio'], row['nome_municipio'], row['populacao_estimada']))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Carga finalizada com sucesso.")

if __name__ == "__main__":
    carregar_populacao()
