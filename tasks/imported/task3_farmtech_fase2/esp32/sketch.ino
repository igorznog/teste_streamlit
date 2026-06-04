// =============================================================================
// FarmTech Solutions — Fase 2
// Sistema de Irrigação Inteligente (ESP32) — Cultura: Café (Coffea arabica)
// Squad WOLF
// =============================================================================
// Sensores simulados no Wokwi:
//   - Botões verdes  -> níveis de N, P, K (true/false)
//   - LDR            -> pH do solo (valor analógico mapeado para 0..14)
//   - DHT22          -> umidade do solo (na prática umidade do ar)
//   - Relé azul      -> bomba d'água
//
// Integração opcional 1 (OpenWeather / Python):
//   O script clima.py envia via Serial uma linha no formato:
//       CHUVA=<0|1>
//   Se CHUVA=1, a irrigação fica suspensa mesmo que as outras condições
//   estejam favoráveis à irrigação.
// =============================================================================

#include <DHT.h>

// -------------------------- Mapeamento de pinos ------------------------------
constexpr uint8_t PIN_BTN_N   = 4;   // botão verde — Nitrogênio
constexpr uint8_t PIN_BTN_P   = 5;   // botão verde — Fósforo
constexpr uint8_t PIN_BTN_K   = 18;  // botão verde — Potássio
constexpr uint8_t PIN_LDR     = 34;  // ADC1_CH6 — LDR representando o pH
constexpr uint8_t PIN_DHT22   = 15;  // DHT22 — umidade do solo (simulada)
constexpr uint8_t PIN_RELE    = 23;  // relé azul — bomba d'água
constexpr uint8_t PIN_LED_INFO = 2;  // LED onboard — pisca no ciclo

// -------------------------- Parâmetros da cultura ----------------------------
// Valores para café arábica (fontes: Embrapa Café / MAPA):
//   - pH ideal do solo: 5.5 a 6.5 (ácido a levemente ácido).
//     Como o enunciado permite ampliar a escala para melhorar a usabilidade
//     do slider do LDR no Wokwi, tratamos a faixa aceitável como 5.0–7.0
//     (ideal 5.5–6.5, tolerância de ±0.5). Isso deixa a janela útil do LDR
//     em aproximadamente 35% do curso do slider.
//   - Umidade do solo: 60% a 80% (abaixo de 60% -> déficit hídrico)
//   - Nutrientes: precisa de pelo menos N + K presentes; P é importante mas
//     geralmente aplicado em correção inicial.
constexpr float PH_MIN       = 5.0f;
constexpr float PH_MAX       = 7.0f;
constexpr float UMID_MIN     = 60.0f;  // abaixo disso, solo seco
constexpr float UMID_MAX     = 80.0f;  // acima disso, solo encharcado
constexpr uint8_t NPK_MIN_OK = 2;      // pelo menos 2 dos 3 nutrientes

// -------------------------- Configuração do DHT22 ----------------------------
#define DHT_TIPO DHT22
DHT dht(PIN_DHT22, DHT_TIPO);

// -------------------------- Estado do sistema --------------------------------
bool bomba_ligada = false;
bool chuva_prevista = false;  // atualizado via Serial pelo clima.py
unsigned long ultimo_log = 0;
constexpr unsigned long INTERVALO_MS = 2000;

// -------------------------- Utilitários --------------------------------------
// Converte leitura do LDR (0..4095) para escala de pH 0..14.
// Observação didática: no projeto real, esta conversão não faz sentido físico;
// é apenas uma convenção de simulação (o aluno ajusta o LDR manualmente para
// refletir o pH "induzido" pela combinação de NPK).
float ldr_para_ph(int leitura_bruta) {
  const float ph = (static_cast<float>(leitura_bruta) / 4095.0f) * 14.0f;
  if (ph < 0.0f) return 0.0f;
  if (ph > 14.0f) return 14.0f;
  return ph;
}

// Lê um botão com pull-up interno. Retorna true se pressionado.
bool botao_pressionado(uint8_t pino) {
  return digitalRead(pino) == LOW;
}

// Processa comandos recebidos via Serial Monitor.
// Formatos aceitos:
//   CHUVA=1  -> há previsão de chuva, suspende irrigação
//   CHUVA=0  -> sem previsão de chuva
void processar_serial() {
  while (Serial.available() > 0) {
    String linha = Serial.readStringUntil('\n');
    linha.trim();
    linha.toUpperCase();
    if (linha.startsWith("CHUVA=")) {
      const String valor = linha.substring(6);
      chuva_prevista = (valor == "1" || valor == "TRUE" || valor == "SIM");
      Serial.print(F(">> Previsão de chuva atualizada: "));
      Serial.println(chuva_prevista ? "SIM" : "NAO");
    }
  }
}

// Lógica central: decide se a bomba deve estar ligada.
bool decidir_irrigacao(bool n_ok, bool p_ok, bool k_ok,
                      float ph, float umidade) {
  const uint8_t nutrientes_presentes =
      (n_ok ? 1 : 0) + (p_ok ? 1 : 0) + (k_ok ? 1 : 0);

  // Regra 0 — chuva: se está chovendo/vai chover, não irriga.
  if (chuva_prevista) return false;

  // Regra 1 — solo encharcado: desliga imediatamente.
  if (umidade >= UMID_MAX) return false;

  // Regra 2 — solo seco (< UMID_MIN):
  //          só liga se pH estiver na faixa e nutrientes suficientes.
  if (umidade < UMID_MIN) {
    const bool ph_ok = (ph >= PH_MIN && ph <= PH_MAX);
    return ph_ok && (nutrientes_presentes >= NPK_MIN_OK);
  }

  // Regra 3 — faixa intermediária (60-80%): só liga se estiver abaixo de 70%
  //          e todos os nutrientes presentes (irrigação preventiva).
  if (umidade < 70.0f && nutrientes_presentes == 3) {
    const bool ph_ok = (ph >= PH_MIN && ph <= PH_MAX);
    return ph_ok;
  }

  return false;
}

// -------------------------- setup / loop -------------------------------------
void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_RELE, OUTPUT);
  pinMode(PIN_LED_INFO, OUTPUT);
  digitalWrite(PIN_RELE, LOW);

  dht.begin();

  Serial.println();
  Serial.println(F("============================================"));
  Serial.println(F(" FarmTech Solutions — Fase 2 (Squad WOLF) "));
  Serial.println(F(" Sistema de Irrigação Inteligente — Café   "));
  Serial.println(F("============================================"));
  Serial.println(F("Envie 'CHUVA=1' ou 'CHUVA=0' via Serial "));
  Serial.println(F("para informar previsão meteorológica.      "));
  Serial.println();
}

void loop() {
  processar_serial();

  if (millis() - ultimo_log < INTERVALO_MS) {
    return;
  }
  ultimo_log = millis();

  const bool n_ok = botao_pressionado(PIN_BTN_N);
  const bool p_ok = botao_pressionado(PIN_BTN_P);
  const bool k_ok = botao_pressionado(PIN_BTN_K);

  const int leitura_ldr = analogRead(PIN_LDR);
  const float ph = ldr_para_ph(leitura_ldr);

  const float umidade = dht.readHumidity();
  const float temperatura = dht.readTemperature();
  const bool dht_ok = !isnan(umidade) && !isnan(temperatura);
  const float umidade_segura = dht_ok ? umidade : 50.0f;

  const bool deve_ligar = decidir_irrigacao(n_ok, p_ok, k_ok,
                                            ph, umidade_segura);

  if (deve_ligar != bomba_ligada) {
    bomba_ligada = deve_ligar;
    digitalWrite(PIN_RELE, bomba_ligada ? HIGH : LOW);
  }

  digitalWrite(PIN_LED_INFO, !digitalRead(PIN_LED_INFO));

  const uint8_t nutrientes_presentes =
      (n_ok ? 1 : 0) + (p_ok ? 1 : 0) + (k_ok ? 1 : 0);
  const bool ph_ok = (ph >= PH_MIN && ph <= PH_MAX);
  const bool npk_ok = (nutrientes_presentes >= NPK_MIN_OK);
  const bool umid_seca = (umidade_segura < UMID_MIN);
  const bool umid_encharcada = (umidade_segura >= UMID_MAX);

  Serial.println(F("----------- LEITURA -----------"));
  Serial.print(F("N: "));   Serial.print(n_ok ? "OK" : "--");
  Serial.print(F("  P: ")); Serial.print(p_ok ? "OK" : "--");
  Serial.print(F("  K: ")); Serial.print(k_ok ? "OK" : "--");
  Serial.print(F("   (")); Serial.print(nutrientes_presentes);
  Serial.print(F("/3, min=")); Serial.print(NPK_MIN_OK);
  Serial.println(F(")"));

  Serial.print(F("LDR bruto: ")); Serial.print(leitura_ldr);
  Serial.print(F("  ->  pH: ")); Serial.print(ph, 2);
  Serial.print(F("  (alvo ")); Serial.print(PH_MIN, 1);
  Serial.print(F("-")); Serial.print(PH_MAX, 1); Serial.println(F(")"));

  if (dht_ok) {
    Serial.print(F("Umidade solo: ")); Serial.print(umidade, 1);
    Serial.print(F("%   Temp: ")); Serial.print(temperatura, 1);
    Serial.println(F(" C"));
  } else {
    Serial.println(F("DHT22 indisponível (usando 50% como fallback)"));
  }
  Serial.print(F("Chuva prevista: "));
  Serial.println(chuva_prevista ? "SIM" : "NAO");

  Serial.println(F("--- Diagnóstico ---"));
  Serial.print(F("  pH dentro da faixa?     "));
  Serial.println(ph_ok ? "SIM" : "NAO");
  Serial.print(F("  NPK suficiente?         "));
  Serial.println(npk_ok ? "SIM" : "NAO");
  Serial.print(F("  Solo seco (<60%)?       "));
  Serial.println(umid_seca ? "SIM" : "NAO");
  Serial.print(F("  Solo encharcado (>=80%)? "));
  Serial.println(umid_encharcada ? "SIM" : "NAO");

  Serial.print(F(">>> BOMBA: "));
  Serial.print(bomba_ligada ? "LIGADA" : "DESLIGADA");
  if (!bomba_ligada) {
    Serial.print(F("   (motivo: "));
    if (chuva_prevista)           Serial.print(F("chuva prevista"));
    else if (umid_encharcada)     Serial.print(F("solo encharcado"));
    else if (!ph_ok)              Serial.print(F("pH fora da faixa"));
    else if (!npk_ok)             Serial.print(F("NPK insuficiente"));
    else if (!umid_seca)          Serial.print(F("umidade suficiente, nao precisa"));
    else                          Serial.print(F("indefinido"));
    Serial.print(F(")"));
  }
  Serial.println();
  Serial.println();
}
