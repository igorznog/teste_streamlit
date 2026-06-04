import streamlit as st
import pandas as pd
import sqlite3
import os
import sys

# IMPORTAR MODULO DO ML
sys.path.append(os.path.abspath(".."))

from ml.predict import predict_risk_score

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="AgroKraken Dashboard",
    layout="wide"
)

st.title("AgroKraken Dashboard")
st.subheader("Monitoramento Inteligente de Operações Agrícolas")

# CONEXÃO COM BANCO SQLITE

db_path = "../data/agrokraken.db"

if not os.path.exists(db_path):
    st.error(
        "Banco de dados não encontrado. Execute primeiro:\n\n"
        "python scripts/ingest_data.py"
    )
    st.stop()

conn = sqlite3.connect(db_path)

try:
    df = pd.read_sql_query(
        "SELECT * FROM operacoes",
        conn
    )
finally:
    conn.close()

# FILTROS

st.sidebar.header("Filtros")

df_filtrado = df.copy()

if "risco_label" in df.columns:

    valores_risco = sorted(
        df["risco_label"].dropna().unique()
    )

    filtro_risco = st.sidebar.multiselect(
        "Nível de risco",
        options=valores_risco,
        default=valores_risco
    )

    df_filtrado = df_filtrado[
        df_filtrado["risco_label"].isin(filtro_risco)
    ]

# MÉTRICAS

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de Operações",
    len(df_filtrado)
)

if "risco_label" in df_filtrado.columns:

    alto_risco = int(
        (df_filtrado["risco_label"] == 1).sum()
    )

    taxa = (
        (alto_risco / len(df_filtrado)) * 100
        if len(df_filtrado) > 0
        else 0
    )

    col2.metric(
        "Operações de Alto Risco",
        alto_risco
    )

    col3.metric(
        "Taxa de Alto Risco",
        f"{taxa:.1f}%"
    )

st.divider()

# DISTRIBUIÇÃO DE RISCO

if "risco_label" in df_filtrado.columns:

    st.subheader("Distribuição de Risco")

    distribuicao = (
        df_filtrado["risco_label"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(distribuicao)

st.divider()

# TABELA

st.subheader("Base de Dados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

st.divider()

# ANÁLISE DO MODELO DE IA

st.subheader("Análise Inteligente do Modelo")

if len(df_filtrado) > 0:

    indice = st.number_input(
        "Selecione o índice da linha para análise",
        min_value=0,
        max_value=len(df_filtrado) - 1,
        value=0,
        step=1
    )

    linha = df_filtrado.iloc[int(indice)].to_dict()

    try:

        resultado = predict_risk_score(linha)

        col1, col2 = st.columns(2)

        col1.metric(
            "Score de Risco",
            resultado["score"]
        )

        col2.metric(
            "Categoria",
            resultado["categoria"].upper()
        )

        st.write("Tipo de risco identificado")
        st.info(resultado["tipo_risco"])

        st.write("Recomendação operacional")
        st.success(resultado["recomendacao"])

    except Exception as erro:

        st.error(
            f"Erro ao executar o modelo: {erro}"
        )

else:

    st.warning(
        "Nenhum registro encontrado com os filtros selecionados."
    )