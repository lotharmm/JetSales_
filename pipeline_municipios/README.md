📊 Pipeline Municipal com Airflow, PostgreSQL e DBeaver
Este projeto executa um pipeline de dados municipais, organizando informações de população, leitos hospitalares e dados do ENEM em um banco PostgreSQL. O fluxo é orquestrado com Airflow e os dados podem ser explorados visualmente via DBeaver.

✅ Requisitos
Docker
Docker Compose
Python 3.10+

DBeaver Community (GUI para banco de dados)

🚀 Passo a Passo
🔧 1. Subindo os serviços com Docker
Clone o repositório:


git clone <https://github.com/lotharmm/JetSales_.git>
cd <JetSales_>

Suba o ambiente com Docker Compose:
docker-compose up -d
Isso inicia o PostgreSQL e o Airflow (se configurado), criando o banco municipios_db.

🐘 2. Instalando e configurando o DBeaver
💾 Instalação
Baixe o DBeaver Community Edition

Instale normalmente conforme o seu sistema operacional:

🔌 Conectando ao banco PostgreSQL do Docker
Abra o DBeaver

Clique em Database > New Database Connection

Escolha PostgreSQL

Preencha os dados da conexão conforme o docker-compose.yml:

Host: localhost

Port: 5433

Database: municipios_db

Username: airflow

Password: airflow_password

Clique em Test Connection

Se for o primeiro uso, o DBeaver pedirá para baixar o driver do PostgreSQL. Aceite.

Clique em Finish

🎉 Agora você está conectado ao banco local do seu Docker via DBeaver.

🐍 3. Executando os scripts Python
Você pode rodar cada script manualmente, com Python local, ou criando tasks no Airflow.

Requisitos locais (caso queira executar no terminal):
pip install psycopg2 pandas

⚙️ Ordem de execução (manual)
1) Download da população (cria CSV ou baixa dados)
python scripts/download/download_populacao.py

2) Carga da população no PostgreSQL
python scripts/load/load_populacao.py

3) Carga de leitos hospitalares
python scripts/load/load_leitos.py

4) Carga dos dados do ENEM
python scripts/load/load_enem.py

5) Testes de qualidade
python scripts/transform/testes_qualidade.py


Cada script realiza uma etapa específica:
- Os arquivos load_*.py inserem dados diretamente nas tabelas do banco.
- O script testes_qualidade.py executa validações nos dados inseridos.

🗂 Estrutura do Projeto
pipeline_municipios/
├── airflow/dags/
│   └── pipeline_municipios.py        # DAG principal do Airflow
├── data/                             # Arquivos baixados, CSVs, etc
├── notebooks/                        # Jupyter notebooks (opcional)
├── scripts/
│   ├── download/
│   │   └── download_populacao.py     # Script de download
│   ├── load/
│   │   ├── load_populacao.py
│   │   ├── load_leitos.py
│   │   └── load_enem.py
│   └── transform/
│       └── testes_qualidade.py
├── sql/
│   └── modelagem.sql                 # Script para criação de tabelas
├── docker-compose.yml               # Infraestrutura com PostgreSQL
└── README.md                        # Este guia
✅ Verificação Final
Todos os containers devem estar rodando:
docker ps

O DBeaver deve exibir as tabelas:
populacao
leitos
enem

Após execução dos scripts:

Você verá os dados nas tabelas

Testes de qualidade aparecerão no log do terminal ou console do Python