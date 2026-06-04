# =============================================================================
# FarmTech Solutions — Consulta climática via Open-Meteo + Estatísticas
#
# Dependência: jsonlite (apenas)
#   install.packages("jsonlite", lib = Sys.getenv("R_LIBS_USER"))
#   Se lib do sistema não for gravável, use lib = Sys.getenv("R_LIBS_USER")
# =============================================================================

library(jsonlite)

# ---------------------------------------------------------------------------
# Parâmetros da consulta (São Paulo como exemplo — região canavieira)
# ---------------------------------------------------------------------------
LATITUDE  <- -23.55
LONGITUDE <- -46.63
VARIAVEL  <- "temperature_2m"   # temperatura a 2 metros do solo

url <- paste0(
  "https://api.open-meteo.com/v1/forecast?",
  "latitude=", LATITUDE,
  "&longitude=", LONGITUDE,
  "&hourly=", VARIAVEL,
  "&timezone=America/Sao_Paulo"
)

cat("Consultando Open-Meteo...\n")
con <- url(url, open = "rt")
on.exit(close(con))
raw  <- readLines(con, warn = FALSE)
close(con)
on.exit(NULL)

dados <- fromJSON(paste(raw, collapse = "\n"))

# ---------------------------------------------------------------------------
# Extrair série temporal de temperatura
# ---------------------------------------------------------------------------
temperaturas <- dados$hourly[[VARIAVEL]]
horarios     <- dados$hourly$time

cat("\nPrimeiros registros:\n")
print(head(data.frame(horario = horarios, temperatura = temperaturas)))

# ---------------------------------------------------------------------------
# Estatísticas descritivas
# ---------------------------------------------------------------------------
media  <- mean(temperaturas, na.rm = TRUE)
desvio <- sd(temperaturas, na.rm = TRUE)
minimo <- min(temperaturas, na.rm = TRUE)
maximo <- max(temperaturas, na.rm = TRUE)

cat("\n========== Estatísticas de Temperatura (°C) ==========\n")
cat(sprintf("  Média         : %.2f\n", media))
cat(sprintf("  Desvio Padrão : %.2f\n", desvio))
cat(sprintf("  Mínima        : %.2f\n", minimo))
cat(sprintf("  Máxima        : %.2f\n", maximo))
cat("======================================================\n")
