import os
import requests

URL = "https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2024/estimativa_dou_2024.xls"
OUTPUT_DIR = "data/raw"
FILENAME = "populacao_2024.xls"

def download_populacao():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, FILENAME)
    
    response = requests.get(URL)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Arquivo salvo em {output_path}")
    else:
        print("Erro no download:", response.status_code)

if __name__ == "__main__":
    download_populacao()
