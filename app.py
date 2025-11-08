import  streamlit as st
from    PIL import Image
import  pandas as pd
import  numpy  as np
import  plotly.express as px
from    utils import *
from    sections.estadisticas   import generar_analisis
from    datetime import datetime, timedelta


# Configuración de la página
st.set_page_config(page_title="Análisis de Estadísticas de Fútbol", layout="wide")

# Título centrado
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
    }
    </style>
    <div class="title">
        Reporte Web Estadísticas Fútbol 
    </div>
    """,
    unsafe_allow_html=True
)

# Lectura de datos
data = cargar_archivos_parquet("data/gold")

df_partido_liga_temp    = data['df_partido_liga_temp']
df_jugadores_stats      = data['df_jugadores_stats']


generar_analisis(df_partido_liga_temp, df_jugadores_stats)

