# =============================================================================
# FarmTech Solutions — Estatísticas sobre os dados das culturas e manejos
#
# Este script lê os CSVs exportados pela aplicação Python (dados_culturas.csv
# e dados_manejos.csv) e calcula estatísticas descritivas: média e desvio padrão.
#
# Sem dependências externas (usa apenas R base).
# =============================================================================

args <- commandArgs(trailingOnly = FALSE)
script_dir <- dirname(sub("--file=", "", args[grep("--file=", args)]))
if (length(script_dir) == 0) script_dir <- "."

CAMINHO_CULTURAS <- file.path(script_dir, "dados_culturas.csv")
CAMINHO_MANEJOS  <- file.path(script_dir, "dados_manejos.csv")

# ---------------------------------------------------------------------------
# Leitura dos dados
# ---------------------------------------------------------------------------
if (!file.exists(CAMINHO_CULTURAS)) {
  stop("Arquivo dados_culturas.csv não encontrado. Execute a exportação no menu Python (opção 10) primeiro.")
}

culturas <- read.csv(CAMINHO_CULTURAS, stringsAsFactors = FALSE)
cat("===== Dados das Culturas =====\n")
print(culturas)

# ---------------------------------------------------------------------------
# Estatísticas — Áreas
# ---------------------------------------------------------------------------
cat("\n===== Estatísticas de Área (m²) =====\n")
cat(sprintf("  Quantidade de registros : %d\n", nrow(culturas)))
cat(sprintf("  Média                   : %.4f\n", mean(culturas$area_ha)))
cat(sprintf("  Desvio Padrão           : %.4f\n", sd(culturas$area_ha)))
cat(sprintf("  Mínimo                  : %.4f\n", min(culturas$area_ha)))
cat(sprintf("  Máximo                  : %.4f\n", max(culturas$area_ha)))

# Estatísticas por tipo de cultura
tipos <- unique(culturas$tipo)
for (tipo in tipos) {
  subset_area <- culturas$area_ha[culturas$tipo == tipo]
  cat(sprintf("\n  [%s]\n", tipo))
  cat(sprintf("    Registros   : %d\n", length(subset_area)))
  cat(sprintf("    Média       : %.4f\n", mean(subset_area)))
  if (length(subset_area) > 1) {
    cat(sprintf("    Desvio Pad. : %.4f\n", sd(subset_area)))
  } else {
    cat("    Desvio Pad. : N/A (apenas 1 registro)\n")
  }
}

# ---------------------------------------------------------------------------
# Estatísticas — Manejos
# ---------------------------------------------------------------------------
if (file.exists(CAMINHO_MANEJOS)) {
  manejos <- read.csv(CAMINHO_MANEJOS, stringsAsFactors = FALSE)

  cat("\n\n===== Dados dos Manejos =====\n")
  print(manejos)

  cat("\n===== Estatísticas de Manejos =====\n")
  cat(sprintf("  Quantidade de registros        : %d\n", nrow(manejos)))
  cat(sprintf("  Média total produto (L)        : %.4f\n", mean(manejos$total_produto_litros)))
  cat(sprintf("  Desvio Padrão total produto (L): %.4f\n", sd(manejos$total_produto_litros)))
  cat(sprintf("  Média dosagem/metro (mL)       : %.2f\n", mean(manejos$dosagem_por_metro)))
  cat(sprintf("  Desvio Padrão dosagem/metro    : %.2f\n", sd(manejos$dosagem_por_metro)))
} else {
  cat("\nArquivo dados_manejos.csv não encontrado. Pulando estatísticas de manejos.\n")
}

cat("\n===== Fim do relatório estatístico =====\n")
