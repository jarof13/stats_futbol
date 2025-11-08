import streamlit      as st
import pandas         as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from   datetime import datetime, timedelta
from   utils import *


def graficas_equipos(df_partido_liga_temp):

    color_discrete_map = {
            "Goles Anotados (Local)": "#1f77b4",       # azul
            "Goles Anotados (Visitante)": "#3399ff",   # azul claro
            "Goles Recibidos (Local)": "#d62728",      # rojo oscuro
            "Goles Recibidos (Visitante)": "#ff6666"   # rojo claro
        }
    df_goles_equipo = generar_tabla_goles(df_partido_liga_temp)
  # Extraer valores únicos ordenados
    temporadas = sorted(df_goles_equipo['temporada'].unique().tolist())
    equipos = sorted(df_goles_equipo['equipo'].unique().tolist())

    # Crear columnas con proporciones 30% / 70%
    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        st.markdown("##### 🗓️ Selecciona una o varias temporadas:")
        temporadas_seleccionadas = st.multiselect(
            "Temporadas",
            options=temporadas,
            default=temporadas[:1],  
            label_visibility="collapsed"  
        )

    with col2:
        st.markdown("##### ⚽ Selecciona uno o varios equipos:")
        equipos_seleccionados = st.multiselect(
            "Equipos",
            options=equipos,
            default="Real Madrid CF",  
            label_visibility="collapsed"
        )
    
    # Filtrar el dataframe según la selección
    df_filtrado = df_goles_equipo[
        (df_goles_equipo['temporada'].isin(temporadas_seleccionadas)) &
        (df_goles_equipo['equipo'].isin(equipos_seleccionados))
    ]

    # Mostrar los resultados en dos columnas
    col_tabla, col_grafico = st.columns([0.45, 0.55])

    # TABLA DE DATOS
    with col_tabla:
        st.markdown("#### Goles por Equipo y Temporada")
            # Etiquetas de columnas
        etiquetas = {
            "liga": "Nombre de la Liga",
            "equipo": "Equipo",
            "goles_hechos_local": "Goles Anotados (Local)",
            "goles_hechos_visitante": "Goles Anotados (Visitante)",
            "goles_recibidos_local": "Goles Recibidos (Local)",
            "goles_recibidos_visitante": "Goles Recibidos (Visitante)",
            "diferencia_goles": "Diferencia de Goles"
        }

        # Seleccionar solo las columnas necesarias
        columnas_tabla = [
            "liga",
            "equipo",
            "goles_hechos_local",
            "goles_hechos_visitante",
            "goles_recibidos_local",
            "goles_recibidos_visitante",
            "diferencia_goles"
        ]

        # Filtrar el DataFrame según esas columnas y renombrarlas
        df_tabla = df_filtrado[columnas_tabla].rename(columns=etiquetas)
        st.dataframe(
            df_tabla,
            use_container_width=True,
            hide_index=True
        )

    # GRÁFICO DE BARRAS
    with col_grafico:
        st.markdown("#### Distribución de Goles Anotados y Recibidos")

        if not df_filtrado.empty:
            # Reorganizar los datos para graficar
            df_melt = df_filtrado.melt(
                id_vars=["temporada", "equipo"],
                value_vars=["goles_hechos_local", "goles_hechos_visitante", 
                            "goles_recibidos_local", "goles_recibidos_visitante", "diferencia_goles"],
                var_name="tipo_gol",
                value_name="cantidad"
            )

            # Etiquetas más legibles
            etiquetas = {
                "goles_hechos_local": "Goles Anotados (Local)",
                "goles_hechos_visitante": "Goles Anotados (Visitante)",
                "goles_recibidos_local": "Goles Recibidos (Local)",
                "goles_recibidos_visitante": "Goles Recibidos (Visitante)",
                "diferencia_goles": "Diferencia de Goles"
            }
            df_melt["tipo_gol"] = df_melt["tipo_gol"].map(etiquetas)

            fig = px.bar(
                df_melt,
                x="equipo",
                y="cantidad",
                color="tipo_gol",
                barmode="group",
                facet_col="temporada",
                title="Goles Anotados y Recibidos por Equipo",
                labels={"cantidad": "Cantidad de Goles", "equipo": "Equipo"},
                color_discrete_map=color_discrete_map
            )

            fig.update_layout(
                font=dict(size=12),
                showlegend=True,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True),
                legend_title_text="Tipo de Gol",
                title_x=0.3
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Selecciona al menos una temporada y un equipo para visualizar el gráfico.")

    

    return temporadas_seleccionadas, equipos_seleccionados


def graficas_jugadores(df_jugadores_stats):

       # Selección de variables relevantes
    vars_principales = [
            'calificacion_general',
            'potencial',
            'aceleracion',
            'velocidad_sprint',
            'regate',
            'control_balon',
            'tiros_largos',
            'agilidad'
        ]

    tab1, tab2, tab3 = st.tabs(["Calificación General por Rango de Edad", "Análisis Descriptivo",
                          "Análisis Multivariable de las Estadísticas de los Jugadores"])

    with tab1:
        st.markdown("### Distribución de Calificación General por Rango de Edad")

        fig = px.box(
            df_jugadores_stats,
            x='calificacion_general',
            y='rango_edad',
            orientation= 'h',
            title='Distribución de Calificación General por Rango de Edad',
            color_discrete_sequence=['blue'],
            labels={
                'rango_edad': 'Rango de Edad',
                'calificacion_general': 'Calificación General',
                'nombre_jugador': 'Jugador'
            },
            hover_data=['nombre_jugador']
        )

        fig.update_layout(
            font=dict(size=14),
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            title=dict(x=0.5, xanchor='center')  # Centrar título
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Estadísticas Descriptivas por Pie Preferido y Rango de Edad")

        # Selector de agrupamiento
        opcion_grupo = st.radio(
            "Selecciona cómo agrupar las estadísticas:",
            ["pie_preferido", "rango_edad"],
            horizontal=True
        )

        # Calcular estadísticas descriptivas
        df_descriptivas = (
            df_jugadores_stats
            .groupby(opcion_grupo)[vars_principales]
            .describe()
            .round(2)
        )

        # Mostrar tabla formateada
        st.dataframe(df_descriptivas, use_container_width=True)

        # También permitir descargar la tabla
        csv = df_descriptivas.to_csv().encode('utf-8')
        st.download_button(
            label="⬇️ Descargar Estadísticas Descriptivas (CSV)",
            data=csv,
            file_name=f"estadisticas_descriptivas_por_{opcion_grupo}.csv",
            mime='text/csv'
        )

    with tab3:
        st.markdown("### Análisis Multivariable de Estadísticas de Jugadores")

        # Selector de color (por pie preferido o rango de edad)
        opcion_color = st.radio(
            "Selecciona la variable para diferenciar los puntos:",
            ["pie_preferido", "rango_edad"],
            horizontal=True
        )

        fig_pair = sns.pairplot(
            df_jugadores_stats[vars_principales + [opcion_color]],
            hue=opcion_color,
            palette="coolwarm",
            diag_kind="kde",
            plot_kws={'alpha': 0.6, 's': 40}
        )

        # Ajustar título general del gráfico
        fig_pair.fig.suptitle(
            "Relaciones entre Atributos de Jugadores",
            y=1.02,
            fontsize=14
        )

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig_pair)
    


