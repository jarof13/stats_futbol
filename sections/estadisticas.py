import streamlit as st
from components.graficos_dashboard    import graficas_equipos
from components.graficos_dashboard    import graficas_jugadores


def generar_analisis(df_partido_liga_temp, df_jugadores_stats):


    # Graficos Equipos
    st.title("Análisis por Equipo y Temporada")
    canal = graficas_equipos(df_partido_liga_temp)


    st.title("Análisis de los Jugador dado su rango de Edad")
    

    # Analisis web
    graficas_jugadores(df_jugadores_stats)