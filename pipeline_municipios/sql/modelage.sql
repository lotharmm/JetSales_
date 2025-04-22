CREATE TABLE public.populacao (
	id serial4 NOT NULL,
	codigo_municipio varchar(1000) NOT NULL,
	nome_municipio varchar(100) NOT NULL,
	populacao_estimada int4 NOT NULL,
	CONSTRAINT populacao_codigo_municipio_key UNIQUE (codigo_municipio),
	CONSTRAINT populacao_pkey PRIMARY KEY (id)
);

CREATE TABLE leitos (
    codigo_municipio VARCHAR(20) PRIMARY KEY,  -- Chave estrangeira para a tabela populacao
    ano INT,
    leitos_totais INT,
    leitos_uti INT,
    leitos_clinicos INT,
    FOREIGN KEY (codigo_municipio) REFERENCES populacao(codigo_municipio)
);


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


-- Inserir dados fictícios na tabela ENEM para cada código de município
INSERT INTO enem (codigo_municipio, ano, nota_media_redacao, nota_media_matematica, nota_media_linguagens, nota_media_ciencias_naturais)
SELECT 
    p.codigo_municipio,
    2024,  -- Ano fictício
    ROUND(RANDOM() * 1000::NUMERIC, 2) AS nota_media_redacao,  -- Nota média fictícia de redação entre 0 e 1000
    ROUND(RANDOM() * 1000::NUMERIC, 2) AS nota_media_matematica,  -- Nota média fictícia de matemática entre 0 e 1000
    ROUND(RANDOM() * 1000::NUMERIC, 2) AS nota_media_linguagens,  -- Nota média fictícia de linguagens entre 0 e 1000
    ROUND(RANDOM() * 1000::NUMERIC, 2) AS nota_media_ciencias_naturais  -- Nota média fictícia de ciências naturais entre 0 e 1000
FROM 
    populacao p;

CREATE TABLE enem (
    id SERIAL PRIMARY KEY,
    codigo_municipio VARCHAR(5) REFERENCES populacao(codigo_municipio),
    ano INTEGER NOT NULL,
    media_matematica NUMERIC(5,2),
    media_linguagens NUMERIC(5,2),
    percentual_participacao NUMERIC(5,2)
);
