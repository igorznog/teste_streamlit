"""
FarmTech Solutions — Menu CLI interativo.

CRUD de culturas + manejo de insumos + exportação CSV.
Dependências: nenhuma externa (apenas stdlib).
"""

from culturas import (
    PRODUTOS_CULTURA,
    criar_cultura,
    listar_culturas,
    buscar_cultura,
    atualizar_cultura,
    deletar_cultura,
    criar_manejo,
    listar_manejos,
    buscar_manejo,
    atualizar_manejo,
    deletar_manejo,
    calcular_manejo,
    exportar_culturas_csv,
    exportar_manejos_csv,
)

MENU = """
=============================================
   FarmTech Solutions — Gestão Agrícola
=============================================
 [CULTURAS]
  1. Cadastrar cultura
  2. Listar culturas
  3. Buscar cultura por ID
  4. Atualizar cultura
  5. Deletar cultura

 [MANEJO DE INSUMOS]
  6. Cadastrar manejo de insumos
  7. Listar manejos
  8. Atualizar manejo
  9. Deletar manejo

 [EXPORTAÇÃO]
  10. Exportar dados para CSV (para uso no R)

  0. Sair
"""


# ---------------------------------------------------------------------------
# Helpers de entrada
# ---------------------------------------------------------------------------
def _ler_tipo() -> str:
    """Solicita o tipo de cultura ao usuário."""
    print("Tipos disponíveis: 1 - Cana-de-açúcar | 2 - Café")
    opcao = input("Escolha (1/2): ").strip()
    if opcao == "1":
        return "Cana-de-açúcar"
    if opcao == "2":
        return "Café"
    raise ValueError("Opção de cultura inválida.")


def _ler_dimensoes(tipo: str) -> dict:
    """Lê as dimensões conforme o tipo da cultura."""
    if tipo == "Cana-de-açúcar":
        comprimento = float(input("Comprimento do terreno (m): "))
        largura = float(input("Largura do terreno (m): "))
        return {"comprimento": comprimento, "largura": largura}
    raio = float(input("Raio da área circular (m): "))
    return {"raio": raio}


# ---------------------------------------------------------------------------
# Ações — CULTURAS
# ---------------------------------------------------------------------------
def acao_cadastrar() -> None:
    tipo = _ler_tipo()
    dims = _ler_dimensoes(tipo)
    cultura = {"tipo": tipo, **dims}
    criar_cultura(cultura)
    print(f"✔ Cultura '{tipo}' cadastrada com sucesso! "
          f"(ID {cultura['id']}, Área: {cultura['area_ha']:.4f} m²)")


def acao_listar() -> None:
    lista = listar_culturas()
    if not lista:
        print("Nenhuma cultura cadastrada.")
        return
    print(f"\n{'ID':<5} {'Tipo':<18} {'Área (m²)':<12}")
    print("-" * 38)
    for c in lista:
        print(f"{c['id']:<5} {c['tipo']:<18} {c['area_ha']:<12.4f}")


def acao_buscar() -> None:
    id_cultura = int(input("ID da cultura: "))
    cultura = buscar_cultura(id_cultura)
    if cultura is None:
        print("Cultura não encontrada.")
        return
    for chave, valor in cultura.items():
        print(f"  {chave}: {valor}")


def acao_atualizar() -> None:
    id_cultura = int(input("ID da cultura a atualizar: "))
    if buscar_cultura(id_cultura) is None:
        print("Cultura não encontrada.")
        return
    tipo = _ler_tipo()
    dims = _ler_dimensoes(tipo)
    dados = {"tipo": tipo, **dims}
    atualizar_cultura(id_cultura, dados)
    print("✔ Cultura atualizada.")


def acao_deletar() -> None:
    id_cultura = int(input("ID da cultura a deletar: "))
    if deletar_cultura(id_cultura):
        print("✔ Cultura removida.")
    else:
        print("Cultura não encontrada.")


# ---------------------------------------------------------------------------
# Ações — MANEJO DE INSUMOS
# ---------------------------------------------------------------------------
def acao_cadastrar_manejo() -> None:
    tipo = _ler_tipo()
    produtos = PRODUTOS_CULTURA[tipo]

    print(f"Produtos disponíveis para {tipo}:")
    for i, prod in enumerate(produtos, 1):
        print(f"  {i}. {prod}")
    idx = int(input("Escolha o produto (número): ")) - 1
    if idx < 0 or idx >= len(produtos):
        raise ValueError("Produto inválido.")
    produto = produtos[idx]

    dosagem = float(input("Dosagem por metro (mL): "))
    num_ruas = int(input("Número de ruas da lavoura: "))
    comprimento_rua = float(input("Comprimento de cada rua (m): "))

    manejo = {
        "cultura_tipo": tipo,
        "produto": produto,
        "dosagem_por_metro": dosagem,
        "num_ruas": num_ruas,
        "comprimento_rua": comprimento_rua,
    }
    criar_manejo(manejo)

    print(f"\n✔ Manejo cadastrado! (ID {manejo['id']})")
    print(f"  Produto        : {produto}")
    print(f"  Metros totais  : {manejo['metros_totais']:.2f} m")
    print(f"  Total produto  : {manejo['total_produto_ml']:.2f} mL "
          f"({manejo['total_produto_litros']:.4f} L)")


def acao_listar_manejos() -> None:
    lista = listar_manejos()
    if not lista:
        print("Nenhum manejo cadastrado.")
        return
    print(f"\n{'ID':<4} {'Cultura':<18} {'Produto':<16} "
          f"{'Dose/m(mL)':<12} {'Ruas':<6} {'Compr(m)':<10} {'Total(L)':<10}")
    print("-" * 80)
    for m in lista:
        print(f"{m['id']:<4} {m['cultura_tipo']:<18} {m['produto']:<16} "
              f"{m['dosagem_por_metro']:<12.1f} {m['num_ruas']:<6} "
              f"{m['comprimento_rua']:<10.1f} {m['total_produto_litros']:<10.4f}")


def acao_atualizar_manejo() -> None:
    id_manejo = int(input("ID do manejo a atualizar: "))
    manejo_atual = buscar_manejo(id_manejo)
    if manejo_atual is None:
        print("Manejo não encontrado.")
        return

    print(f"Manejo atual: {manejo_atual['produto']} em {manejo_atual['cultura_tipo']}")
    dosagem = float(input("Nova dosagem por metro (mL): "))
    num_ruas = int(input("Novo número de ruas: "))
    comprimento_rua = float(input("Novo comprimento de cada rua (m): "))

    dados = {
        "dosagem_por_metro": dosagem,
        "num_ruas": num_ruas,
        "comprimento_rua": comprimento_rua,
    }
    atualizar_manejo(id_manejo, dados)
    print("✔ Manejo atualizado.")


def acao_deletar_manejo() -> None:
    id_manejo = int(input("ID do manejo a deletar: "))
    if deletar_manejo(id_manejo):
        print("✔ Manejo removido.")
    else:
        print("Manejo não encontrado.")


# ---------------------------------------------------------------------------
# Exportação
# ---------------------------------------------------------------------------
def acao_exportar() -> None:
    exportados = []
    try:
        caminho = exportar_culturas_csv()
        exportados.append(f"  Culturas → {caminho}")
    except ValueError as e:
        print(f"  Culturas: {e}")

    try:
        caminho = exportar_manejos_csv()
        exportados.append(f"  Manejos  → {caminho}")
    except ValueError as e:
        print(f"  Manejos: {e}")

    if exportados:
        print("✔ Exportação concluída:")
        for linha in exportados:
            print(linha)


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------
ACOES = {
    "1":  acao_cadastrar,
    "2":  acao_listar,
    "3":  acao_buscar,
    "4":  acao_atualizar,
    "5":  acao_deletar,
    "6":  acao_cadastrar_manejo,
    "7":  acao_listar_manejos,
    "8":  acao_atualizar_manejo,
    "9":  acao_deletar_manejo,
    "10": acao_exportar,
}


def main() -> None:
    while True:
        print(MENU)
        opcao = input("Opção: ").strip()
        if opcao == "0":
            print("Encerrando. Até logo!")
            break
        acao = ACOES.get(opcao)
        if acao is None:
            print("Opção inválida. Tente novamente.")
            continue
        try:
            acao()
        except (ValueError, KeyError) as e:
            print(f"Erro de entrada: {e}")


if __name__ == "__main__":
    main()
