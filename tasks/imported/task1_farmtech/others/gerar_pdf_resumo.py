"""Gera resumo_artigo.pdf com formatação FIAP: Arial 11, espaçamento simples, margens 2cm."""
from fpdf import FPDF

TITULO = (
    "USO DE VEÍCULOS AÉREOS NÃO TRIPULADOS (VANT) "
    "EM AGRICULTURA DE PRECISÃO"
)
SUBTITULO = (
    "Resumo do Capítulo 8 - JORGE, L. A. C.; INAMASU, R. Y. "
    "Embrapa Instrumentação, São Carlos, SP."
)

TEXTO = (
    "O capítulo aborda o uso de Veículos Aéreos Não Tripulados (VANTs), também conhecidos como drones, "
    "como ferramenta emergente na agricultura de precisão. Os autores contextualizam o crescimento global "
    "do interesse por essas aeronaves, impulsionado por avanços em tecnologia computacional, miniaturização "
    "de sensores, materiais mais leves e sistemas de navegação por GPS. O Japão se destaca com mais de "
    "2.000 VANTs aplicados na agricultura, enquanto no Brasil os primeiros desenvolvimentos ocorreram na "
    "década de 1980, com destaque para o projeto ARARA da Embrapa, voltado ao monitoramento de áreas "
    "agrícolas por meio de fotografias aéreas.\n\n"

    "O artigo descreve os componentes de um VANT: a aeronave em si, a estação de controle em solo (GCS), "
    "o sistema GPS, a unidade de navegação inercial (IMU) e o piloto automático (AFCS). Em conjunto, esses "
    "elementos permitem o planejamento e execução de missões autônomas de monitoramento. Os VANTs são "
    "classificados quanto ao tipo de asa (fixa, rotativa ou multirotor), cada um com vantagens e desvantagens "
    "em termos de custo, transporte, condições climáticas e capacidade de carga. Os multirotores se destacam "
    "para uso agrícola por permitirem decolagem vertical, voo estacionário e operação em espaços restritos, "
    "apesar da autonomia de bateria limitada a cerca de 30 minutos.\n\n"

    "Uma parte significativa do capítulo é dedicada aos sensores embarcados. São apresentadas quatro "
    "categorias principais: câmeras no espectro visível (RGB), que permitem identificar falhas de plantio e "
    "acompanhar o desenvolvimento das culturas; sensores no infravermelho próximo (NIR), usados para gerar "
    "índices de vegetação como o NDVI, que indica estresse hídrico e nutricional; sensores hiperespectrais, "
    "que capturam centenas de bandas do espectro eletromagnético e permitem identificar propriedades "
    "bioquímicas como clorofila, nitrogênio e lignina; e câmeras térmicas, utilizadas para detectar estresse "
    "hídrico por meio do mapeamento de temperatura do dossel vegetal.\n\n"

    "Os autores apresentam um fluxo de trabalho em sete etapas para o uso de VANTs na agricultura de "
    "precisão: planejamento de voo, voo com sobreposição de imagens, obtenção de imagens "
    "georreferenciadas, processamento das imagens, geração de mosaicos, análise em ferramentas GIS e "
    "geração de relatórios. Detalhes técnicos são discutidos, como a relação entre altitude de voo e resolução "
    "do pixel, sobreposição mínima de 60%% para mosaicos de qualidade, e cuidados com velocidade de "
    "obturador para evitar borramentos.\n\n"

    "Na conclusão, os autores ressaltam que, apesar de estarem em fase de regulamentação pela ANAC, os "
    "VANTs se tornam cada vez mais acessíveis e confiáveis. Os desafios principais ainda envolvem "
    "manutenção inadequada, condições de operação em campo e a necessidade de padronização regulatória. "
    "Entretanto, a tendência é que os drones se consolidem como uma das ferramentas mais úteis na "
    "agricultura de precisão, democratizando o acesso ao sensoriamento remoto que antes dependia "
    "exclusivamente de satélites e aeronaves tripuladas."
)

RODAPE = (
    "Higor Henrique Garcia - RM 571820 - FIAP 2026\n"
    "Fase 1 - Agricultura Digital / Formação Social"
)

FONT_PATH = "/mnt/c/Windows/Fonts/"

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()
pdf.set_margins(20, 20, 20)

pdf.add_font("Arial", "", FONT_PATH + "arial.ttf", uni=True)
pdf.add_font("Arial", "B", FONT_PATH + "arialbd.ttf", uni=True)
pdf.add_font("Arial", "I", FONT_PATH + "ariali.ttf", uni=True)

pdf.set_font("Arial", "B", 11)
pdf.multi_cell(0, 5, TITULO, align="C")
pdf.ln(2)

pdf.set_font("Arial", "I", 9)
pdf.multi_cell(0, 4, SUBTITULO, align="C")
pdf.ln(4)

pdf.set_font("Arial", "", 11)
for paragrafo in TEXTO.split("\n\n"):
    pdf.multi_cell(0, 5, paragrafo.strip(), align="J")
    pdf.ln(1)

pdf.ln(3)
pdf.set_font("Arial", "I", 9)
pdf.multi_cell(0, 4, RODAPE, align="C")

pdf.output("resumo_artigo.pdf")
print("PDF gerado: resumo_artigo.pdf")
