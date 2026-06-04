"""Gera o relatório PDF da Task 2 — Teachable Machine."""
from fpdf import FPDF

FONT_PATH = "/mnt/c/Windows/Fonts/"

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(20, 20, 20)

pdf.add_font("Arial", "", FONT_PATH + "arial.ttf")
pdf.add_font("Arial", "B", FONT_PATH + "arialbd.ttf")
pdf.add_font("Arial", "I", FONT_PATH + "ariali.ttf")
pdf.add_font("Arial", "BI", FONT_PATH + "arialbi.ttf")

def titulo(txt):
    pdf.set_font("Arial", "B", 14)
    pdf.multi_cell(0, 8, txt)
    pdf.ln(2)

def subtitulo(txt):
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 7, txt)
    pdf.ln(1)

def corpo(txt):
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 5.5, txt, align="J")
    pdf.ln(1)

def italico(txt):
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 5, txt)
    pdf.ln(1)

def placeholder_print(label):
    pdf.set_font("Arial", "BI", 10)
    pdf.set_fill_color(235, 235, 245)
    pdf.multi_cell(0, 12, f"  >>> {label} <<<", border=1, align="C", fill=True)
    pdf.ln(3)

# --- CAPA ---
pdf.add_page()
pdf.ln(40)
pdf.set_font("Arial", "B", 18)
pdf.cell(0, 10, "Higor Henrique Garcia", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Arial", "", 13)
pdf.cell(0, 8, "RM: 571820", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(12)
pdf.set_font("Arial", "B", 15)
pdf.multi_cell(0, 8, "Fase 1 - Capítulo 2\nIA e seu mundo de possibilidades", align="C")
pdf.ln(10)
pdf.set_font("Arial", "", 13)
pdf.multi_cell(0, 7, (
    "Relatório de Estudo de Caso\n"
    "Classificação de Utensílios de Cozinha\n"
    "com Teachable Machine (Google)"
), align="C")
pdf.ln(25)
pdf.set_font("Arial", "I", 11)
pdf.cell(0, 6, "FIAP - Março 2026", align="C", new_x="LMARGIN", new_y="NEXT")

# --- 1. OBJETIVOS ---
pdf.add_page()
titulo("1. Objetivos")
corpo(
    "Este trabalho teve como objetivos: (i) desenvolver um modelo de visão computacional "
    "capaz de classificar fotografias de utensílios de cozinha em categorias pré-definidas; "
    "(ii) aplicar conceitos básicos de aprendizado de máquina supervisionado; "
    "(iii) utilizar a ferramenta Teachable Machine para treinar e validar o modelo sem "
    "necessidade de código; e (iv) avaliar o desempenho do modelo por meio de testes "
    "com imagens não utilizadas no treinamento, comparando diferentes configurações "
    "de hiperparâmetros."
)

# --- 2. METODOLOGIA ---
titulo("2. Metodologia")

subtitulo("2.1 Coleta e organização dos dados")
corpo(
    "Foram definidas três classes de utensílios de cozinha: Panelas, Talheres e "
    "Utensílios de Preparo. As imagens foram obtidas por meio de fotografias realizadas "
    "em ambiente doméstico, utilizando um smartphone Samsung Galaxy S24 Ultra. "
    "As fotos foram tiradas com boa iluminação, foco nítido no objeto e fundo neutro "
    "(bancada de granito escuro), evitando elementos que pudessem interferir na detecção."
)
corpo(
    "O conjunto de dados foi organizado da seguinte forma:\n"
    "  - Panelas: 21 imagens (panelas e frigideiras em diferentes ângulos)\n"
    "  - Talheres: 42 imagens (garfos, facas e colheres em variações de modelo)\n"
    "  - Utensílios de Preparo: 21 imagens (espátulas, conchas, colheres de pau)\n\n"
    "De cada classe, foram reservadas imagens para o conjunto de teste, garantindo que "
    "não fossem utilizadas durante o treinamento."
)

subtitulo("2.2 Ferramenta e configuração do modelo")
corpo(
    "Utilizou-se o Teachable Machine (Google), acessível em "
    "https://teachablemachine.withgoogle.com, selecionando a opção 'Image Project' "
    "com 'Standard image model'. As imagens de treino foram carregadas por classe. "
    "Foram realizados dois experimentos com configurações avançadas distintas:"
)

pdf.set_font("Arial", "B", 10)
col_w = [35, 30, 30, 35, 40]
headers = ["Experimento", "Epochs", "Batch Size", "Learning Rate", "Observação"]
for i, h in enumerate(headers):
    pdf.cell(col_w[i], 7, h, border=1, align="C")
pdf.ln()
pdf.set_font("Arial", "", 10)
for row in [
    ["1 (baseline)", "50", "16", "0,001", "Padrão da ferramenta"],
    ["2 (ajuste)", "100", "16", "0,001", "Dobro de épocas"],
]:
    for i, val in enumerate(row):
        pdf.cell(col_w[i], 7, val, border=1, align="C")
    pdf.ln()
pdf.ln(4)

placeholder_print("Print 1: Tela do Teachable Machine com as 3 classes e amostras de imagens carregadas")

# --- 3. DESENVOLVIMENTO ---
titulo("3. Desenvolvimento do Experimento")
corpo(
    "O desenvolvimento seguiu as seguintes etapas:\n\n"
    "1. Criação do projeto no Teachable Machine e definição das três classes com nomes "
    "descritivos: Panelas, Talheres e Utensilios_de_Preparo.\n\n"
    "2. Upload das imagens de treinamento em cada classe. A classe Talheres recebeu "
    "um volume maior de imagens (42) por conta da maior variedade de objetos nessa "
    "categoria (garfos, facas de diferentes tamanhos, colheres de sopa e de chá). "
    "As classes Panelas e Utensílios de Preparo receberam 21 imagens cada.\n\n"
    "3. Primeiro treinamento (Experimento 1) com os parâmetros padrão: 50 epochs, "
    "batch size 16, learning rate 0,001. A ferramenta processou as imagens e gerou "
    "um modelo de classificação baseado em transfer learning.\n\n"
    "4. Teste rápido do Experimento 1 utilizando a webcam, apresentando uma faca "
    "à câmera para verificar se o modelo respondia corretamente.\n\n"
    "5. Segundo treinamento (Experimento 2) com o dobro de épocas (100), mantendo "
    "batch size e learning rate idênticos, para observar o efeito na precisão.\n\n"
    "6. Teste completo do Experimento 2, apresentando três objetos diferentes "
    "(colher de pau, frigideira e faca) à webcam, um por vez."
)

placeholder_print("Print 2: Configurações avançadas do treinamento (Epochs, Batch Size, Learning Rate)")

# --- 4. TESTES E AVALIAÇÃO ---
pdf.add_page()
titulo("4. Testes e Avaliação")

subtitulo("4.1 Resultados do Experimento 1 (50 epochs)")
corpo(
    "Após o primeiro treinamento, foi realizado um teste rápido apresentando uma faca "
    "à webcam. O modelo classificou corretamente como Talheres com confiança de 96%."
)

placeholder_print("Print 3: Teste do Experimento 1 - Faca classificada como Talheres (96%)")

subtitulo("4.2 Resultados do Experimento 2 (100 epochs)")
corpo(
    "Após o segundo treinamento com o dobro de épocas, foram testados três objetos "
    "distintos via webcam:"
)

pdf.set_font("Arial", "B", 10)
tcol = [50, 50, 35, 35]
theaders = ["Objeto testado", "Classificação", "Confiança", "Acertou?"]
for i, h in enumerate(theaders):
    pdf.cell(tcol[i], 7, h, border=1, align="C")
pdf.ln()
pdf.set_font("Arial", "", 10)
for row in [
    ["Colher de pau", "Utens. de Preparo", "100%", "Sim"],
    ["Frigideira", "Panelas", "100%", "Sim"],
    ["Faca", "Talheres", "94%", "Sim"],
]:
    for i, val in enumerate(row):
        pdf.cell(tcol[i], 7, val, border=1, align="C")
    pdf.ln()
pdf.ln(4)

placeholder_print("Print 4: Teste Experimento 2 - Colher de pau classificada como Utensílios (100%)")
placeholder_print("Print 5: Teste Experimento 2 - Frigideira classificada como Panelas (100%)")
placeholder_print("Print 6: Teste Experimento 2 - Faca classificada como Talheres (94%)")

subtitulo("4.3 Comparação entre experimentos")
corpo(
    "Para o mesmo objeto (faca), os resultados foram:\n"
    "  - Experimento 1 (50 epochs): Talheres com 96% de confiança\n"
    "  - Experimento 2 (100 epochs): Talheres com 94% de confiança\n\n"
    "Ambos classificaram corretamente, porém o Experimento 1 apresentou confiança "
    "ligeiramente superior (96% vs. 94%). Essa diferença, embora pequena, pode indicar "
    "um princípio de overfitting no Experimento 2: com mais épocas, o modelo se "
    "especializou demais nas imagens de treinamento, perdendo uma fração de "
    "capacidade de generalização para imagens novas."
)

# --- 5. JUSTIFICATIVA ---
titulo("5. Justificativa Técnica dos Resultados")
corpo(
    "O desempenho elevado do modelo pode ser explicado pelos seguintes fatores:\n\n"
    "1. Qualidade e consistência dos dados: as imagens foram fotografadas no mesmo "
    "ambiente, com iluminação e fundo consistentes, facilitando a extração de "
    "características relevantes do objeto pelo modelo.\n\n"
    "2. Diferenciação visual entre classes: panelas possuem forma arredondada e "
    "tamanho grande; talheres são alongados e metálicos; utensílios de preparo "
    "variam entre madeira e silicone. Essa distinção visual reduz a confusão.\n\n"
    "3. Volume adequado de dados: com 21 a 42 imagens por classe e variação de "
    "ângulo, o modelo conseguiu generalizar para objetos apresentados ao vivo.\n\n"
    "4. Hiperparâmetros: 50 epochs foram suficientes para convergência dada a "
    "simplicidade do problema (3 classes visualmente distintas). O aumento para "
    "100 epochs não trouxe melhoria, confirmando que o modelo já havia convergido.\n\n"
    "5. A pequena queda de confiança da faca (96% para 94%) ao dobrar epochs reforça "
    "o conceito de que mais treinamento nem sempre é melhor - o equilíbrio entre "
    "underfitting e overfitting é fundamental em aprendizado de máquina."
)

# --- 6. ANÁLISE CRÍTICA ---
pdf.add_page()
titulo("6. Análise Crítica e Sugestões de Melhoria")
corpo(
    "Limitações identificadas neste estudo:\n\n"
    "- Conjunto de dados reduzido: embora suficiente para três classes distintas, um "
    "cenário com mais categorias ou objetos visualmente similares exigiria conjuntos "
    "maiores (50+ imagens por classe).\n\n"
    "- Ambiente controlado: o modelo foi treinado com imagens de um único ambiente. "
    "Em cenários reais com iluminação variável, fundos diferentes ou múltiplos objetos "
    "na cena, o desempenho poderia ser inferior.\n\n"
    "- Desbalanceamento de classes: a classe Talheres (42 imagens) teve o dobro das "
    "demais (21 cada), o que pode introduzir viés a favor dessa classe.\n\n"
    "- Teste limitado: apenas 3 objetos foram testados por classe. Uma avaliação "
    "estatisticamente robusta exigiria um conjunto de teste maior.\n\n"
    "Sugestões de melhoria:\n\n"
    "- Aumentar o número de imagens por classe com variação de fundo, iluminação "
    "e distância.\n"
    "- Balancear as classes para evitar viés.\n"
    "- Incluir uma classe 'Outros' para evitar classificações forçadas.\n"
    "- Exportar o modelo e avaliá-lo com métricas de precisão, revocação e F1-score.\n"
    "- Testar com imagens de outros dispositivos e ambientes para validar "
    "generalização."
)

# --- 7. CONCLUSÃO ---
titulo("7. Conclusão")
corpo(
    "O Teachable Machine permitiu construir um classificador de imagens de forma "
    "rápida e acessível, cumprindo os objetivos de familiarização com aprendizado de "
    "máquina e visão computacional. Os resultados foram satisfatórios, com acurácia "
    "de 100% nos testes e confiança entre 94% e 100%. A comparação entre os dois "
    "experimentos evidenciou que o aumento de épocas não trouxe melhoria "
    "significativa, e até reduziu levemente a confiança em um dos casos, reforçando "
    "a importância do ajuste adequado de hiperparâmetros. As oportunidades de "
    "melhoria identificadas servem como direcionamento para projetos futuros com "
    "maior complexidade e robustez."
)

# --- REFERÊNCIAS ---
pdf.add_page()
titulo("Referências")
corpo(
    "Google. Teachable Machine. Disponível em: https://teachablemachine.withgoogle.com. "
    "Acesso em: 24 mar. 2026."
)

pdf.output("HigorHenriqueGarcia_RM571820_fase1_cap2.pdf")
print("PDF gerado: HigorHenriqueGarcia_RM571820_fase1_cap2.pdf")
