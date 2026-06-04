# =============================================================================
# FarmTech Solutions — Fase 2 — Opcional 2 (R)
# Análise estatística das leituras de umidade e pH para recomendar irrigação.
# Squad WOLF
# =============================================================================
#
# Entrada:  leituras_exemplo.csv  (timestamp, n, p, k, ph, umidade, bomba)
# Saída:    console — estatísticas descritivas + teste t + recomendação final.
#
# Lógica:
#   1. Calcula média e desvio padrão de pH e umidade.
#   2. Compara a média de umidade com o limiar ideal do café (70%) via
#      teste t de uma amostra (H0: média >= 70%).
#   3. Se a hipótese for rejeitada (p-valor < 0.05 e média < 70), recomenda
#      LIGAR a bomba. Caso contrário, recomenda DESLIGAR.
#   4. Também gera um boxplot PNG (opcional) em graficos/.
#
# Execução:
#   Rscript irrigacao_stats.R
#   Rscript irrigacao_stats.R caminho/para/arquivo.csv
# =============================================================================

args <- commandArgs(trailingOnly = TRUE)

# Descobre o diretório do próprio script (robusto com Rscript).
this_file <- NULL
cmd_args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", cmd_args, value = TRUE)
if (length(file_arg) > 0) {
  this_file <- sub("^--file=", "", file_arg[1])
}
script_dir <- if (!is.null(this_file) && nzchar(this_file)) {
  normalizePath(dirname(this_file))
} else {
  getwd()
}

csv_path <- if (length(args) >= 1) args[1] else file.path(script_dir, "leituras_exemplo.csv")

cat("============================================================\n")
cat(" FarmTech Fase 2 — Análise Estatística de Irrigação (R)\n")
cat(" Cultura: Café (Coffea arabica)\n")
cat("============================================================\n\n")

if (!file.exists(csv_path)) {
  stop(sprintf("Arquivo de leituras não encontrado: %s", csv_path))
}

dados <- read.csv(csv_path, stringsAsFactors = FALSE)
cat(sprintf("Arquivo: %s\n", csv_path))
cat(sprintf("Total de leituras: %d\n\n", nrow(dados)))

cat("--- Amostra (6 primeiras linhas) ---\n")
print(utils::head(dados))
cat("\n")

# ----- Estatísticas descritivas ---------------------------------------------
media_umid <- mean(dados$umidade, na.rm = TRUE)
sd_umid    <- sd(dados$umidade, na.rm = TRUE)
media_ph   <- mean(dados$ph, na.rm = TRUE)
sd_ph      <- sd(dados$ph, na.rm = TRUE)

cat("--- Estatísticas descritivas ---\n")
cat(sprintf("Umidade (%%)  : média = %5.2f  | desvio = %5.2f\n", media_umid, sd_umid))
cat(sprintf("pH simulado  : média = %5.2f  | desvio = %5.2f\n", media_ph, sd_ph))

ph_min_cafe <- 5.5
ph_max_cafe <- 6.5
umid_alvo   <- 70.0  # % ideal para café

cat("\n--- Faixas ideais para café ---\n")
cat(sprintf("pH     : %.1f a %.1f\n", ph_min_cafe, ph_max_cafe))
cat(sprintf("Umidade: >= %.0f%% (alvo); evitar < 60%% ou > 80%%\n\n", umid_alvo))

# ----- Teste t: média de umidade vs alvo ------------------------------------
cat("--- Teste t (H0: média da umidade >= 70%) ---\n")
teste <- tryCatch(
  t.test(dados$umidade, mu = umid_alvo, alternative = "less"),
  error = function(e) NULL
)

if (!is.null(teste)) {
  cat(sprintf("t = %.3f | df = %.1f | p-valor = %.4f\n",
              teste$statistic, teste$parameter, teste$p.value))
  cat(sprintf("IC 95%%: [%.2f, %.2f]\n",
              teste$conf.int[1], teste$conf.int[2]))
} else {
  cat("Não foi possível rodar o teste t (variância zero?).\n")
}

# ----- Decisão final ---------------------------------------------------------
ph_ok <- media_ph >= ph_min_cafe & media_ph <= ph_max_cafe
umid_baixa <- media_umid < umid_alvo
p_significativo <- !is.null(teste) && teste$p.value < 0.05

recomenda_ligar <- umid_baixa && p_significativo && ph_ok

cat("\n============================================================\n")
if (recomenda_ligar) {
  cat(" RECOMENDAÇÃO: LIGAR a bomba de irrigação.\n")
  cat(" Justificativa: umidade média significativamente abaixo de 70% e\n")
  cat(" pH dentro da faixa ideal para café.\n")
} else {
  cat(" RECOMENDAÇÃO: DESLIGAR / manter bomba desligada.\n")
  cat(" Justificativa: ")
  if (!umid_baixa) cat("umidade média dentro/acima do alvo. ")
  if (!ph_ok) cat("pH médio fora da faixa ideal do café. ")
  if (!p_significativo && !is.null(teste)) cat("evidência estatística fraca. ")
  cat("\n")
}
cat("============================================================\n")

# ----- Boxplot opcional (se a plataforma permitir) --------------------------
graficos_dir <- file.path(script_dir, "graficos")
if (!dir.exists(graficos_dir)) dir.create(graficos_dir, showWarnings = FALSE)

tryCatch({
  png(file.path(graficos_dir, "boxplot_umidade_ph.png"),
      width = 800, height = 500, res = 110)
  par(mfrow = c(1, 2))
  boxplot(dados$umidade, main = "Umidade do solo (%)",
          col = "#4E9F3D", ylab = "%")
  abline(h = c(60, 80), col = "red", lty = 2)
  boxplot(dados$ph, main = "pH simulado",
          col = "#D8E9A8", ylab = "pH")
  abline(h = c(ph_min_cafe, ph_max_cafe), col = "red", lty = 2)
  dev.off()
  cat(sprintf("\n[ok] Gráfico salvo em %s/boxplot_umidade_ph.png\n",
              graficos_dir))
}, error = function(e) {
  cat(sprintf("\n[aviso] não foi possível gerar gráfico: %s\n", e$message))
})
