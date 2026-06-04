-- ============================================================================
-- FarmTech Fase 3 - Cap 1 - Consultas demonstrativas (rubrica: 2,0 pts)
-- ============================================================================
-- Rode cada bloco no Oracle SQL Developer e tire prints separados.
-- Sugestão de prints para o README:
--   prints/sql_01_select_all.png       -> Q1
--   prints/sql_02_total_leituras.png   -> Q2
--   prints/sql_03_bomba_perc.png       -> Q4
--   prints/sql_04_ph_por_hora.png      -> Q6
--   prints/sql_05_alertas.png          -> Q8
-- ============================================================================

-- Q1) Conferência rápida: 10 primeiras leituras importadas
SELECT *
FROM   leituras_sensores
WHERE  ROWNUM <= 10
ORDER  BY ts;

-- Q2) Total de leituras na tabela (deve bater com o CSV - 1 cabeçalho)
SELECT COUNT(*) AS total_leituras FROM leituras_sensores;

-- Q3) Estatísticas descritivas de pH e umidade
SELECT ROUND(MIN(ph),2)       AS ph_min,
       ROUND(MAX(ph),2)       AS ph_max,
       ROUND(AVG(ph),2)       AS ph_medio,
       ROUND(STDDEV(ph),2)    AS ph_desvio,
       ROUND(MIN(umidade),1)  AS umid_min,
       ROUND(MAX(umidade),1)  AS umid_max,
       ROUND(AVG(umidade),1)  AS umid_media,
       ROUND(STDDEV(umidade),1) AS umid_desvio
FROM   leituras_sensores;

-- Q4) Percentual de tempo com a bomba ligada
SELECT SUM(bomba)                                 AS leituras_bomba_on,
       COUNT(*)                                   AS total,
       ROUND(SUM(bomba)*100/COUNT(*), 2)          AS pct_bomba_on
FROM   leituras_sensores;

-- Q5) Distribuição de N, P, K (qual nutriente está mais presente?)
SELECT SUM(n) AS n_total,
       SUM(p) AS p_total,
       SUM(k) AS k_total,
       COUNT(*) AS leituras
FROM   leituras_sensores;

-- Q6) Média de pH e umidade por hora do dia (perfil diário)
SELECT EXTRACT(HOUR FROM ts)    AS hora,
       ROUND(AVG(ph), 2)        AS ph_medio_hora,
       ROUND(AVG(umidade), 1)   AS umid_media_hora,
       COUNT(*)                 AS leituras
FROM   leituras_sensores
GROUP  BY EXTRACT(HOUR FROM ts)
ORDER  BY hora;

-- Q7) Leituras com pH fora da faixa do café (5.5 a 6.5) — possíveis alertas
SELECT ts, ph, umidade, n, p, k, bomba
FROM   leituras_sensores
WHERE  ph NOT BETWEEN 5.5 AND 6.5
ORDER  BY ts
FETCH  FIRST 20 ROWS ONLY;

-- Q8) Alertas críticos: solo seco (umidade < 50%) E bomba desligada
SELECT ts, umidade, ph, n, p, k
FROM   leituras_sensores
WHERE  umidade < 50
  AND  bomba   = 0
ORDER  BY ts
FETCH  FIRST 20 ROWS ONLY;

-- Q9) Quantos eventos contínuos de irrigação (transições 0->1) ocorreram?
WITH transicoes AS (
   SELECT ts, bomba,
          LAG(bomba) OVER (ORDER BY ts) AS bomba_anterior
   FROM   leituras_sensores
)
SELECT COUNT(*) AS num_eventos_irrigacao
FROM   transicoes
WHERE  bomba = 1 AND NVL(bomba_anterior, 0) = 0;

-- Q10) Top 5 períodos mais críticos (umidade mais baixa) por janela de 1h
SELECT TO_CHAR(TRUNC(CAST(ts AS DATE), 'HH24'), 'YYYY-MM-DD HH24:00') AS janela_hora,
       ROUND(AVG(umidade), 1) AS umid_media,
       COUNT(*)               AS leituras
FROM   leituras_sensores
GROUP  BY TRUNC(CAST(ts AS DATE), 'HH24')
ORDER  BY umid_media ASC
FETCH  FIRST 5 ROWS ONLY;
