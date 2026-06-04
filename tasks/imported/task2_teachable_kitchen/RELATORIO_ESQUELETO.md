> **Uso**: Copiar para Word/Google Docs. Trocar textos entre `[COLAR]`. Inserir prints onde indicado. Exportar como `HigorHenriqueGarcia_RM571820_fase1_cap2.pdf`.

---

**Capa (centralizar)**

**Higor Henrique Garcia**  
RM: 571820  
Fase 1 — Capítulo 2 — IA e seu mundo de possibilidades  

**Relatório de estudo de caso**  
Classificação de utensílios de cozinha com Teachable Machine (Google)

---

## 1. Objetivos

Este trabalho teve como objetivos: (i) desenvolver um modelo de visão computacional capaz de classificar fotografias de utensílios de cozinha em categorias pré-definidas; (ii) aplicar conceitos básicos de aprendizado de máquina supervisionado; (iii) utilizar a ferramenta Teachable Machine para treinar e validar o modelo sem necessidade de código; (iv) avaliar o desempenho do modelo por meio de métricas exibidas na plataforma e de testes com imagens não usadas no treinamento.

---

## 2. Metodologia

### 2.1 Coleta e organização dos dados

Foram definidas **três classes**: [COLAR: ex. Talheres / Panelas / Utensílios de preparo].

A coleta seguiu [COLAR: "fotografias realizadas em ambiente doméstico" OU "imagens selecionadas de repositório Pexels/Unsplash com licença de uso livre"]. As imagens foram obtidas com [COLAR: boa iluminação / fundo neutro / foco no objeto], evitando, quando possível, objetos estranhos ao centro da cena.

O conjunto foi dividido em:
- **Treinamento**: [COLAR: N] imagens no total ([COLAR: n1] classe 1, [COLAR: n2] classe 2, [COLAR: n3] classe 3).
- **Teste**: [COLAR: M] imagens reservadas, **não** utilizadas no treinamento, para avaliar generalização.

### 2.2 Ferramenta e configuração do modelo

Utilizou-se o **Teachable Machine** (Google), projeto **Classificação de Imagem** → **Imagem Padrão** (Standard image model), em [COLAR: navegador Chrome / Edge], no endereço https://teachablemachine.withgoogle.com .

As imagens de treino foram carregadas por classe. Em seguida foram ajustados parâmetros em **Configurações avançadas**, conforme tabela abaixo.

| Experimento | Épocas (epochs) | Batch size | Learning rate | Observação |
|-------------|-----------------|------------|---------------|------------|
| 1 | [COLAR] | [COLAR] | [COLAR] | [COLAR: ex. baseline] |
| 2 | [COLAR] | [COLAR] | [COLAR] | [COLAR: ex. mais épocas] |

*[INSERIR PRINT 1: tela do Teachable Machine com as classes e amostras de imagens]*

*[INSERIR PRINT 2: treinamento concluído com métrica de acurácia / loss visível]*

O modelo foi treinado com o botão **Treinar Modelo**; o tempo de treino foi de aproximadamente [COLAR: X minutos] em cada execução.

---

## 3. Desenvolvimento do experimento (passo a passo)

1. Criação do projeto e definição das três classes com nomes claros.
2. Upload das imagens de treino por classe, mantendo balanceamento aproximado entre classes.
3. Ajuste de hiperparâmetros (épocas, batch size, learning rate) e novo treinamento para comparar comportamento.
4. Utilização da seção **Preview** / **Webcam** (ou upload de arquivo) para classificar imagens do conjunto de teste.
5. Registro de acertos e erros qualitativos (confusão entre classes mais parecidas).

---

## 4. Testes e avaliação

### 4.1 Resultados no conjunto de teste

Foram submetidas [COLAR: M] imagens de teste. O modelo classificou corretamente [COLAR: K] casos, resultando em **acurácia aproximada de [COLAR: K/M × 100]%** nesse subconjunto manual.

**Exemplos de acerto:** [COLAR: descrever 1–2 casos].

**Exemplos de erro:** [COLAR: descrever 1–2 casos — ex. confundir colher de servir com talher de mesa].

*[INSERIR PRINT 3: tela de teste com previsões e confiança]*

### 4.2 Métricas na interface

Ao final do treinamento, a interface exibiu **acurácia** [COLAR: ex. 0,XX ou XX%] no conjunto de treino/validação interno da ferramenta. *[Ajustar conforme o que o Teachable Machine mostrar — loss, se visível.]*

---

## 5. Justificativa técnica dos resultados

O desempenho obtido pode ser explicado por:

1. **Quantidade e variedade de dados**: classes com poucas imagens ou pouca variação de ângulo e iluminação tendem a **overfitting**, ou seja, o modelo memoriza o treino e falha no teste.
2. **Semelhança visual entre classes**: objetos de metal reflexivo ou formas parecidas aumentam a taxa de confusão.
3. **Hiperparâmetros**: aumentar **épocas** pode melhorar o ajuste até certo ponto; depois disso pode piorar generalização. **Batch size** e **learning rate** influenciam a estabilidade do treino (gradiente mais ou menos ruidoso).

No experimento [COLAR: 1 ou 2], observou-se [COLAR: melhor pior resultado / métrica mais alta], o que sugere que [COLAR: uma frase].

---

## 6. Análise crítica e sugestões de melhoria

**Limitações deste estudo:** conjunto de dados reduzido em ambiente não controlado; possível desbalanceamento entre classes; métricas dependem da interface do Teachable Machine.

**Melhorias sugeridas:**
- Aumentar o número de imagens por classe (≥30) com variação de ângulo, distância e fundo.
- Incluir dados negativos ou “outros” se o modelo confundir objetos irrelevantes.
- Testar iluminação mais uniforme (fundo branco ou preto).
- Para um trabalho futuro: exportar o modelo e avaliar em um conjunto de teste maior com métricas precisão/revocação por classe.

---

## 7. Conclusão

O Teachable Machine permitiu construir um classificador de imagens de forma **rápida e didática**, atendendo aos objetivos de familiarização com **aprendizado de máquina** e **visão computacional**. Os resultados obtidos foram [COLAR: satisfatórios / mistos], com oportunidades claras de melhoria na **qualidade e diversidade** dos dados.

---

## Referências

Google. *Teachable Machine*. Disponível em: https://teachablemachine.withgoogle.com. Acesso em: 24 mar. 2026.

[COLAR: se usou Pexels/Unsplash, citar o repositório e a data de acesso.]

---

*Fim do relatório.*
