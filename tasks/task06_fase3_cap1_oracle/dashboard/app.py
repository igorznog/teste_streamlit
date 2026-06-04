"""Dashboard FarmTech — Fase 3 Cap 1 — Ir Além Opção 1 (+5 pts).

Visualiza as leituras do ESP32 (Fase 2) e sugere irrigação com base na
mesma lógica do sketch.ino. Cumpre a rubrica:
  - Visualização clara de ≥3 variáveis: umidade, pH, P/K  (1,5 pt)
  - Interatividade/Visualização Streamlit                  (1,0 pt)
  - Integração com dados da Fase 2                          (1,0 pt)
  - Documentação no GitHub                                  (0,5 pt)
  - Vídeo demonstrativo                                     (1,0 pt)

Uso:
    pip install -r requirements.txt
    streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

CSV_PADRAO = Path(__file__).parent.parent / "dados" / "leituras_sensores.csv"
FAIXA_PH_CAFE = (5.5, 6.5)
FAIXA_PH_BOMBA = (5.0, 7.0)
UMIDADE_BAIXA = 60
UMIDADE_ALTA = 80


def sugerir_irrigacao(umidade: float, ph: float, npk_total: int, chuva_prevista: bool) -> str:
    if chuva_prevista:
        return "🌧 Suspensa — chuva prevista"
    if umidade >= UMIDADE_ALTA:
        return "✋ Não irrigar — solo encharcado"
    ph_ok = FAIXA_PH_BOMBA[0] <= ph <= FAIXA_PH_BOMBA[1]
    if umidade < UMIDADE_BAIXA:
        if ph_ok and npk_total >= 2:
            return "💧 Ligar bomba — solo seco e nutrientes ok"
        return "⚠ Não irrigar — pH fora da faixa ou faltam nutrientes"
    if umidade < 70:
        if ph_ok and npk_total == 3:
            return "💧 Irrigar preventivamente — todos os nutrientes ok"
        return "✋ Não irrigar — aguardar mais umidade"
    return "✋ Não irrigar — umidade adequada"


@st.cache_data(show_spinner=False)
def carregar_dados(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df["npk_total"] = df["n"] + df["p"] + df["k"]
    df["hora"] = df["timestamp"].dt.hour
    df["dia"] = df["timestamp"].dt.date
    return df


def main() -> None:
    st.set_page_config(
        page_title="FarmTech — Dashboard Fase 3 Cap 1",
        page_icon="🌱",
        layout="wide",
    )
    st.title("🌱 FarmTech Solutions — Dashboard de Irrigação")
    st.caption("Fase 3 Cap 1 — Ir Além Opção 1 (Dashboard Python/Streamlit). "
               "Dados: ESP32 simulado no Wokwi (Fase 2), cultura **café (Coffea arabica)**.")

    with st.sidebar:
        st.header("⚙ Configuração")
        csv_path = st.text_input("Arquivo CSV", value=str(CSV_PADRAO))
        chuva_prevista = st.checkbox("☔ Chuva prevista (suspende irrigação)",
                                     value=False)
        st.divider()
        st.markdown(
            "**Faixas ideais (café):**\n"
            f"- pH: {FAIXA_PH_CAFE[0]}–{FAIXA_PH_CAFE[1]}\n"
            f"- Umidade: {UMIDADE_BAIXA}%–{UMIDADE_ALTA}%\n"
            "- N + K altos, P moderado"
        )

    try:
        df = carregar_dados(csv_path)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {csv_path}")
        st.info("Rode: `python3 dados/gerar_dataset.py` para criar o dataset.")
        return

    # === MÉTRICAS ===
    ultima = df.iloc[-1]
    sugestao = sugerir_irrigacao(
        ultima["umidade"], ultima["ph"], int(ultima["npk_total"]), chuva_prevista
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📅 Leituras", f"{len(df):,}")
    col2.metric("💧 Umidade atual", f"{ultima['umidade']:.1f}%",
                delta=f"{ultima['umidade'] - df['umidade'].mean():+.1f}% vs. média")
    col3.metric("🧪 pH atual", f"{ultima['ph']:.2f}",
                delta=f"{ultima['ph'] - df['ph'].mean():+.2f} vs. média")
    col4.metric("🌾 NPK presente", f"{int(ultima['npk_total'])}/3")
    col5.metric("🔌 Bomba (média)",
                f"{df['bomba'].mean() * 100:.1f}%")

    if "Ligar" in sugestao or "Irrigar" in sugestao:
        st.success(f"**Sugestão da última leitura:** {sugestao}")
    elif "Suspensa" in sugestao:
        st.info(f"**Sugestão da última leitura:** {sugestao}")
    else:
        st.warning(f"**Sugestão da última leitura:** {sugestao}")

    # === FILTRO TEMPORAL ===
    st.divider()
    st.subheader("🔎 Filtro temporal")
    janela = st.slider(
        "Janela (últimas N leituras)",
        min_value=50,
        max_value=len(df),
        value=min(500, len(df)),
        step=50,
    )
    df_view = df.tail(janela)

    # === GRÁFICOS ===
    tabs = st.tabs(["📈 Umidade & pH", "🌾 NPK", "🔌 Bomba", "📊 Tabela"])

    with tabs[0]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_view["timestamp"], y=df_view["umidade"],
            mode="lines", name="Umidade (%)", line=dict(color="#1f77b4"),
        ))
        fig.add_trace(go.Scatter(
            x=df_view["timestamp"], y=df_view["ph"],
            mode="lines", name="pH", yaxis="y2", line=dict(color="#ff7f0e"),
        ))
        fig.add_hrect(y0=UMIDADE_BAIXA, y1=UMIDADE_ALTA,
                      fillcolor="green", opacity=0.1,
                      annotation_text="Faixa ideal de umidade", annotation_position="top left")
        fig.update_layout(
            title="Umidade e pH ao longo do tempo",
            xaxis_title="Tempo",
            yaxis=dict(title="Umidade (%)", range=[20, 100]),
            yaxis2=dict(title="pH", overlaying="y", side="right", range=[3, 10]),
            hovermode="x unified",
            height=480,
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        df_npk = pd.DataFrame({
            "nutriente": ["Nitrogênio (N)", "Fósforo (P)", "Potássio (K)"],
            "presenca_pct": [
                df_view["n"].mean() * 100,
                df_view["p"].mean() * 100,
                df_view["k"].mean() * 100,
            ],
        })
        col_a, col_b = st.columns([1, 1])
        with col_a:
            fig = px.bar(df_npk, x="nutriente", y="presenca_pct",
                         color="nutriente", title="% de leituras com cada nutriente presente",
                         range_y=[0, 100], text="presenca_pct")
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            fig = px.histogram(df_view, x="npk_total", nbins=4,
                               title="Distribuição da soma N+P+K por leitura",
                               labels={"npk_total": "Nutrientes presentes"})
            st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        bomba_por_hora = (df_view.groupby("hora")["bomba"].mean() * 100).reset_index()
        bomba_por_hora.columns = ["hora", "pct_bomba_on"]
        fig = px.bar(bomba_por_hora, x="hora", y="pct_bomba_on",
                     title="% do tempo com bomba ligada, por hora do dia",
                     labels={"hora": "Hora", "pct_bomba_on": "Bomba ligada (%)"})
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        eventos = df_view["bomba"].diff().fillna(0)
        n_ativacoes = int((eventos > 0).sum())
        n_desligamentos = int((eventos < 0).sum())
        c1, c2, c3 = st.columns(3)
        c1.metric("🔼 Ativações da bomba", n_ativacoes)
        c2.metric("🔽 Desligamentos", n_desligamentos)
        c3.metric("⏱ Tempo ligado", f"{(df_view['bomba'].sum() * 2) / 60:.1f} h",
                  help="Assumindo 1 leitura a cada 2 minutos.")

    with tabs[3]:
        st.dataframe(
            df_view[["timestamp", "n", "p", "k", "ph", "umidade", "bomba"]]
            .sort_values("timestamp", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "📥 Baixar visualização atual (CSV)",
            data=df_view.to_csv(index=False).encode("utf-8"),
            file_name="leituras_filtradas.csv",
            mime="text/csv",
        )

    st.divider()
    st.caption(
        "Dashboard FarmTech — Fase 3 Cap 1 — Grupo Cap 10 (Vinicius, Higor, Igor, Humberto). "
        "Lógica de irrigação alinhada ao `esp32/sketch.ino` da Fase 2."
    )


if __name__ == "__main__":
    main()
