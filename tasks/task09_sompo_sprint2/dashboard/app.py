import streamlit as st
import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

# AJUSTE DE PATH PARA STREAMLIT CLOUD

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# IMPORTAR MÓDULO DO ML

from ml.predict import predict_risk_score

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="AgroKraken Dashboard",
    layout="wide"
)

st.title("AgroKraken Dashboard")
st.subheader("Monitoramento Inteligente de Operações Agrícolas")

# CONEXÃO COM BANCO SQLITE

db_path = ROOT_DIR / "data" / "agrokraken.db"

if not db_path.exists():
    st.error(
        "Banco de dados não encontrado. Execute primeiro:\n\n"
        "python scripts/ingest_data.py"
    )
    st.stop()

conn = sqlite3.connect(db_path)