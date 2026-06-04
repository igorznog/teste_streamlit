"""
Módulo de cálculo de área e manejo de insumos para as culturas da FarmTech Solutions.

Culturas suportadas:
  - Cana-de-açúcar (área retangular: comprimento × largura)
  - Café (área circular: π × raio²)

Os dados são armazenados em listas de dicionários (vetores),
conforme exigido pelas diretrizes do projeto.
"""

import math
import csv
import os

# ---------------------------------------------------------------------------
# Vetores principais (listas de dicionários)
# ---------------------------------------------------------------------------
culturas: list[dict] = []
manejos: list[dict] = []

# ---------------------------------------------------------------------------
# Constantes de produto por cultura (exemplos reais simplificados)
# ---------------------------------------------------------------------------
PRODUTOS_CULTURA = {
    "Cana-de-açúcar": ["Herbicida", "Fertilizante NPK", "Inseticida"],
    "Café":           ["Fosfato", "Fungicida", "Adubo foliar"],
}

CAMINHO_CSV = os.path.join(os.path.dirname(__file__), "dados_culturas.csv")
CAMINHO_MANEJOS_CSV = os.path.join(os.path.dirname(__file__), "dados_manejos.csv")


# ========================== CÁLCULOS DE ÁREA ===============================

def calcular_area(cultura: dict) -> float:
    """Retorna a área plantada de acordo com o tipo da cultura."""
    tipo = cultura["tipo"]
    if tipo == "Cana-de-açúcar":
        return cultura["comprimento"] * cultura["largura"]
    if tipo == "Café":
        return math.pi * cultura["raio"] ** 2
    return 0.0


# ======================== MANEJO DE INSUMOS ================================

def calcular_manejo(manejo: dict) -> dict:
    """
    Calcula o total de insumo necessário para o manejo.

    Lógica: o usuário informa dosagem por metro (mL ou g), o número de ruas
    da lavoura e o comprimento de cada rua. O sistema calcula:
      - metros_totais = num_ruas × comprimento_rua
      - total_produto = dosagem_por_metro × metros_totais
    """
    metros_totais = manejo["num_ruas"] * manejo["comprimento_rua"]
    total_produto = manejo["dosagem_por_metro"] * metros_totais
    return {
        "metros_totais": round(metros_totais, 2),
        "total_produto_ml": round(total_produto, 2),
        "total_produto_litros": round(total_produto / 1000, 4),
    }


# ========================== CRUD — CULTURAS ================================

def _proximo_id(lista: list[dict]) -> int:
    """Gera o próximo ID sequencial para uma lista."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def criar_cultura(cultura: dict) -> None:
    """Adiciona uma cultura ao vetor."""
    cultura["id"] = _proximo_id(culturas)
    cultura["area_ha"] = calcular_area(cultura)
    culturas.append(cultura)


def listar_culturas() -> list[dict]:
    """Retorna todas as culturas cadastradas."""
    return culturas


def buscar_cultura(id_cultura: int) -> dict | None:
    """Busca uma cultura pelo ID."""
    for c in culturas:
        if c["id"] == id_cultura:
            return c
    return None


def atualizar_cultura(id_cultura: int, dados: dict) -> bool:
    """Atualiza os campos de uma cultura existente."""
    cultura = buscar_cultura(id_cultura)
    if cultura is None:
        return False
    cultura.update(dados)
    cultura["area_ha"] = calcular_area(cultura)
    return True


def deletar_cultura(id_cultura: int) -> bool:
    """Remove uma cultura pelo ID."""
    cultura = buscar_cultura(id_cultura)
    if cultura is None:
        return False
    culturas.remove(cultura)
    return True


# ========================== CRUD — MANEJOS =================================

def criar_manejo(manejo: dict) -> None:
    """Adiciona um registro de manejo ao vetor."""
    manejo["id"] = _proximo_id(manejos)
    resultado = calcular_manejo(manejo)
    manejo.update(resultado)
    manejos.append(manejo)


def listar_manejos() -> list[dict]:
    """Retorna todos os manejos cadastrados."""
    return manejos


def buscar_manejo(id_manejo: int) -> dict | None:
    """Busca um manejo pelo ID."""
    for m in manejos:
        if m["id"] == id_manejo:
            return m
    return None


def atualizar_manejo(id_manejo: int, dados: dict) -> bool:
    """Atualiza um manejo existente e recalcula totais."""
    manejo = buscar_manejo(id_manejo)
    if manejo is None:
        return False
    manejo.update(dados)
    resultado = calcular_manejo(manejo)
    manejo.update(resultado)
    return True


def deletar_manejo(id_manejo: int) -> bool:
    """Remove um manejo pelo ID."""
    manejo = buscar_manejo(id_manejo)
    if manejo is None:
        return False
    manejos.remove(manejo)
    return True


# ========================== EXPORTAÇÃO CSV =================================

def exportar_culturas_csv() -> str:
    """Exporta o vetor de culturas para CSV. Retorna o caminho do arquivo."""
    if not culturas:
        raise ValueError("Nenhuma cultura cadastrada para exportar.")

    campos = ["id", "tipo", "area_ha"]
    with open(CAMINHO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(culturas)
    return CAMINHO_CSV


def exportar_manejos_csv() -> str:
    """Exporta o vetor de manejos para CSV. Retorna o caminho do arquivo."""
    if not manejos:
        raise ValueError("Nenhum manejo cadastrado para exportar.")

    campos = [
        "id", "cultura_tipo", "produto", "dosagem_por_metro",
        "num_ruas", "comprimento_rua", "metros_totais",
        "total_produto_ml", "total_produto_litros",
    ]
    with open(CAMINHO_MANEJOS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(manejos)
    return CAMINHO_MANEJOS_CSV
