-- ============================================================================
-- FarmTech Fase 3 - Cap 1 - Banco de Dados Oracle
-- DDL: tabela LEITURAS_SENSORES (dados do ESP32 da Fase 2)
-- ============================================================================
-- Schema dos sensores Wokwi/ESP32:
--   timestamp -> momento da leitura (TIMESTAMP)
--   n,p,k     -> presença de Nitrogênio, Fósforo, Potássio (0|1)
--   ph        -> pH do solo (0..14, café ideal 5.5–6.5)
--   umidade   -> % de umidade (0..100, café ideal 60–80)
--   bomba     -> estado da bomba após a regra de irrigação (0|1)
--
-- Observação: este script pode ser executado ANTES do wizard "Importar Dados"
-- se você preferir criar a tabela manualmente. O wizard também cria a tabela
-- automaticamente — neste caso, pule o CREATE TABLE.
-- ============================================================================

-- limpa execução anterior (idempotente)
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE leituras_sensores CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN RAISE; END IF;  -- ORA-00942: tabela inexistente
END;
/

CREATE TABLE leituras_sensores (
   id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   ts            TIMESTAMP        NOT NULL,
   n             NUMBER(1)        NOT NULL,   -- 0 ou 1
   p             NUMBER(1)        NOT NULL,
   k             NUMBER(1)        NOT NULL,
   ph            NUMBER(4,2)      NOT NULL,   -- 0.00 a 14.00
   umidade       NUMBER(5,2)      NOT NULL,   -- 0.00 a 100.00
   bomba         NUMBER(1)        NOT NULL,   -- 0 ou 1
   CONSTRAINT ck_n_bool       CHECK (n IN (0,1)),
   CONSTRAINT ck_p_bool       CHECK (p IN (0,1)),
   CONSTRAINT ck_k_bool       CHECK (k IN (0,1)),
   CONSTRAINT ck_bomba_bool   CHECK (bomba IN (0,1)),
   CONSTRAINT ck_ph_range     CHECK (ph BETWEEN 0 AND 14),
   CONSTRAINT ck_umid_range   CHECK (umidade BETWEEN 0 AND 100)
);

COMMENT ON TABLE  leituras_sensores             IS 'Leituras dos sensores do ESP32 (FarmTech Fase 2) - cultura café.';
COMMENT ON COLUMN leituras_sensores.ts          IS 'Momento da leitura (timestamp).';
COMMENT ON COLUMN leituras_sensores.n           IS 'Presença de Nitrogênio (1 = presente).';
COMMENT ON COLUMN leituras_sensores.p           IS 'Presença de Fósforo (1 = presente).';
COMMENT ON COLUMN leituras_sensores.k           IS 'Presença de Potássio (1 = presente).';
COMMENT ON COLUMN leituras_sensores.ph          IS 'pH do solo (0..14, café ideal 5.5-6.5).';
COMMENT ON COLUMN leituras_sensores.umidade     IS 'Umidade do solo em % (0..100, café ideal 60-80).';
COMMENT ON COLUMN leituras_sensores.bomba       IS 'Estado da bomba (1 = ligada).';

-- índices para acelerar filtros temporais e por estado da bomba
CREATE INDEX ix_leituras_ts    ON leituras_sensores(ts);
CREATE INDEX ix_leituras_bomba ON leituras_sensores(bomba);

-- valida criação
SELECT table_name, num_rows FROM user_tables WHERE table_name = 'LEITURAS_SENSORES';
DESC leituras_sensores
