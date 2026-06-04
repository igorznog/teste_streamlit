# Fundamentação Agronômica — FarmTech Fase 2

> Documento de apoio que justifica, com base na literatura cafeeira
> brasileira, cada decisão da lógica de irrigação implementada no
> `sketch.ino`. Cultura: **café arábica (*Coffea arabica*)**.

---

## 1. Exigências edafoclimáticas do café arábica

### 1.1 pH do solo — **ideal 5.5 a 6.5**

O café arábica é uma cultura adaptada a solos **ácidos a levemente ácidos**.
A maior parte do parque cafeeiro brasileiro está em **latossolos**, que têm
pH natural entre 4.5 e 5.5 — por isso o manejo clássico inclui **calagem**
(aplicação de calcário dolomítico) para corrigir a acidez e elevar o pH à
faixa ideal.

| Faixa de pH | Consequência agronômica |
|-------------|-------------------------|
| < 5.0 | **Toxicidade por alumínio** (Al³⁺ solúvel) — queima radicular, absorção paralisada |
| 5.0 – 5.5 | Aceitável; ainda pode haver limitação de Ca e Mg |
| **5.5 – 6.5** | **Faixa ideal** — alta disponibilidade de N, P, K, Ca, Mg |
| 6.5 – 7.0 | Aceitável; começa a bloquear micronutrientes |
| > 7.0 | **Bloqueio de Fe, Mn, Zn, B, Cu** — clorose férrica, folhas amareladas |

**Referências**:
- Malavolta, E. (2006) *Manual de Nutrição Mineral de Plantas*.
- Matiello, J. B. et al. (2020) *Cultura do Café no Brasil — Novo Manual de
  Recomendações*. Fundação Procafé.
- IAC — Boletim 100 (Recomendações de adubação e calagem para o estado de
  São Paulo).

### 1.2 Umidade do solo — **ideal 60–80% da capacidade de campo**

A água é o fator climático mais limitante da produtividade cafeeira. O
café arábica é extremamente sensível em **duas fases fenológicas**:

| Fase | Período | Impacto da falta de água |
|------|---------|--------------------------|
| **Florada** | Set–Out | Abortamento de flores ("chumbinho"); menor pegamento |
| **Granação** | Out–Mar | Grãos chochos, pequenos; pior classificação e bebida |

Acima de 80% de umidade (encharcamento):
- Raízes sofrem **hipóxia** (baixa oxigenação)
- Ambiente favorável a fungos: ***Phytophthora***, ***Rosellinia bunodes***,
  ***Fusarium oxysporum***
- Morte radicular progressiva → tombamento da planta

**Referência**: Camargo, A. P. (2010) *A seca e o café no Brasil*. Boletim
Técnico IAC.

### 1.3 NPK — demanda anual de um cafezal em produção

Lavoura adulta produzindo ~30 sacas/ha/ano:

| Nutriente | Demanda (kg/ha/ano) | Papel fisiológico |
|-----------|---------------------|-------------------|
| **N** | 300–400 | Proteínas, clorofila, crescimento vegetativo |
| **K** | 250–350 | Enchimento dos grãos, qualidade de bebida, resistência a stress hídrico e doenças |
| **P** | 20–40 | Crítico na **formação** (raízes); em lavoura adulta, aplicações de manutenção |

Fórmulas comerciais típicas: **20-05-20** ou **20-00-20** (N alto, K alto,
P baixo). É por isso que no código definimos `NPK_MIN_OK = 2` — **N e K são
os nutrientes indispensáveis**; P entra como reforço.

**Referência**: Guimarães, P. T. G. et al. (1999) *Cafeeiro — Recomendações
para o uso de corretivos e fertilizantes em Minas Gerais*. CFSEMG.

---

## 2. Relação entre adubação NPK e pH do solo

### 2.1 Afinal, NPK acidifica ou alcaliniza?

**Resposta: em termos práticos, as fontes comerciais de NPK mais usadas
ACIDIFICAM o solo ao longo do tempo.** Entender isso é essencial para
justificar a manipulação combinada das chaves NPK e do slider LDR no Wokwi.

### 2.2 Mecanismo 1 — Nitrificação

As fontes nitrogenadas mais comuns (ureia, sulfato de amônio, MAP, DAP)
liberam amônio no solo, que é oxidado por bactérias (*Nitrosomonas*,
*Nitrobacter*):

$$\text{NH}_4^+ + 2\,\text{O}_2 \rightarrow \text{NO}_3^- + 2\,\text{H}^+ + \text{H}_2\text{O}$$

Cada mol de amônio libera **2 mols de H⁺** → acidificação.

### 2.3 Mecanismo 2 — Balanço de cátions/ânions na absorção

Para manter neutralidade elétrica, a raiz expele na rizosfera o oposto do
íon que absorve:

- Absorve cátion (K⁺, Ca²⁺, NH₄⁺) → expele **H⁺** (acidifica)
- Absorve ânion (NO₃⁻, SO₄²⁻, H₂PO₄⁻) → expele **OH⁻** (alcaliniza)

No balanço líquido de um cafezal adubado, o volume de cátions absorvidos
supera o de ânions → **acidificação líquida**.

### 2.4 Efeito comparado das fontes de adubo

| Fonte | Efeito no pH | Potencial de acidificação (kg CaCO₃ eq. por 100 kg) |
|-------|--------------|-----------------------------------------------------|
| Sulfato de amônio | Acidifica muito | ~110 |
| Ureia | Acidifica moderado | ~80 |
| MAP (P + N amoniacal) | Acidifica leve | ~60 |
| DAP | Acidifica leve | ~40 |
| Cloreto de potássio (KCl) | Quase neutro | ~0 |
| Nitrato de cálcio | Alcaliniza leve | negativo |

**Conclusão prática para o projeto**: cada vez que o operador liga uma
chave NPK no Wokwi, é agronomicamente coerente **arrastar o slider do LDR
para a esquerda** (simular queda de pH). A recuperação do pH depende de
**calagem** (ação externa, que o operador simula arrastando o slider para
a direita).

**Referências**:
- Raij, B. van (2011) *Fertilidade do Solo e Manejo de Nutrientes*. IPNI.
- Sousa, D. M. G.; Lobato, E. (2004) *Cerrado: correção do solo e
  adubação*. Embrapa.

---

## 3. Justificativa regra a regra da lógica de irrigação

A função `decidir_irrigacao(...)` em `sketch.ino` implementa o fluxograma
abaixo. Cada regra é comentada com base nas seções 1 e 2.

### Regra 0 — Chuva prevista → **bomba desligada**
- **Fonte**: API OpenWeather (opcional 1) ou comando `CHUVA=1` via Serial.
- **Justificativa**: irrigar com chuva a caminho causa **duplo desperdício**
  (água + energia) e aumenta risco de encharcamento/erosão. Boa prática de
  agricultura de precisão.

### Regra 1 — Umidade ≥ 80% → **bomba desligada**
- **Justificativa**: encharcamento leva à hipóxia radicular e à
  proliferação de *Phytophthora* e *Rosellinia*. Em café adulto, solo
  encharcado por 48h já pode causar morte de raízes finas.

### Regra 2 — Umidade < 60% + pH ∈ [5.0, 7.0] + NPK ≥ 2 → **bomba ligada**
- **Umidade < 60%**: déficit hídrico, fora da faixa ótima de 60–80%.
- **pH ∈ [5.0, 7.0]**: faixa ampliada (ideal 5.5–6.5) para acomodar a
  usabilidade do slider do LDR. Fora disso, a planta não absorveria bem
  os nutrientes mesmo recebendo água — irrigação seria desperdício.
- **NPK ≥ 2**: pelo menos N e K presentes. Em lavoura faminta de nutrientes,
  água sozinha não produz resposta produtiva.

### Regra 3 — 60% ≤ Umidade < 70% + pH ok + NPK = 3 → **bomba ligada (preventiva)**
- **Justificativa**: em fases críticas (florada, granação) vale manter a
  umidade próxima ao ótimo (~80%) para não comprometer pegamento e
  enchimento de grãos. Só acionamos essa irrigação **preventiva** se a
  lavoura estiver **totalmente nutrida** (os 3 nutrientes presentes) —
  caso contrário, irrigar sem NPK completo não teria retorno produtivo.

### Regra implícita — pH fora da faixa → **bomba desligada (mesmo com solo seco)**
- **Decisão consciente do projeto**: prioriza economia de recursos.
- **Agronômico**: se o pH está ruim, a planta não aproveita bem a água
  nem os nutrientes. Em campo, a resposta correta é corrigir pH (calagem
  ou acidificação) antes de intensificar a irrigação.
- **Alternativa**: em uma versão mais permissiva, poderíamos irrigar mesmo
  com pH ruim para aliviar stress hídrico — optamos pela versão
  conservadora, coerente com o lema da FarmTech: "otimização de recursos".

---

## 4. Como manipular o simulador Wokwi de forma agronomicamente coerente

| Ação desejada (conceito) | No Wokwi |
|--------------------------|----------|
| Simular aplicação de **N** (ureia, sulfato de amônio) | Ligar chave `N` + arrastar slider do LDR levemente à **esquerda** (pH cai) |
| Simular aplicação de **K** (KCl) | Ligar chave `K` + **não mexer muito no LDR** (KCl é quase neutro) |
| Simular aplicação de **P** (MAP, SSP) | Ligar chave `P` + arrastar LDR levemente à **esquerda** |
| Simular **calagem** (correção de acidez) | Arrastar LDR à **direita** (pH sobe para ~6.0) |
| Simular **solo sem adubação nem calagem** (natural) | Chaves desligadas + LDR na **esquerda** (pH ~5.0 ou abaixo, típico de latossolo) |
| Simular **chuva natural** | Subir Humidity do DHT22 para > 80% |
| Simular **verão seco** | Humidity < 40% |
| Simular **previsão meteorológica de chuva** | Digitar `CHUVA=1` no Serial Monitor |

---

## 5. Possíveis evoluções futuras (Fase 3?)

- **Fertirrigação inteligente**: acoplar dosador de adubo ao sistema, medir
  EC (condutividade elétrica) para não aplicar adubo em excesso.
- **Modelo preditivo de pH**: usar histórico de adubações + dias desde a
  última calagem para prever pH sem sensor físico.
- **Integração com estações meteorológicas locais** (INMET, CEMADEN) em
  vez de API global.
- **Zoneamento da lavoura**: sensores por talhão, irrigação setorizada.

---

## 6. Referências

1. Malavolta, E. (2006). *Manual de Nutrição Mineral de Plantas*. Agronômica
   Ceres.
2. Matiello, J. B.; Santinato, R.; Garcia, A. W. R.; Almeida, S. R.;
   Fernandes, D. R. (2020). *Cultura do Café no Brasil — Novo Manual de
   Recomendações*. Fundação Procafé.
3. Raij, B. van (2011). *Fertilidade do Solo e Manejo de Nutrientes*.
   International Plant Nutrition Institute (IPNI).
4. Sousa, D. M. G.; Lobato, E. (2004). *Cerrado: correção do solo e
   adubação*. Embrapa Informação Tecnológica.
5. Guimarães, P. T. G. et al. (1999). *Recomendações para o uso de
   corretivos e fertilizantes em Minas Gerais — 5ª Aproximação*. CFSEMG.
6. Camargo, A. P. (2010). *A seca e o café no Brasil*. Boletim Técnico IAC.
7. IAC (1996). *Boletim 100 — Recomendações de adubação e calagem para o
   estado de São Paulo*.
8. Embrapa Café — *Portal do Café* (https://www.embrapa.br/cafe).
