import pandas         as pd
import numpy          as np 
import plotly.express as px
import streamlit      as st
import os



def cargar_archivos_parquet(carpeta: str) -> dict[str, pd.DataFrame]:
    """
    Lee todos los archivos Parquet de una carpeta y devuelve un diccionario de DataFrames.

    Args:
        carpeta (str): Ruta a la carpeta donde se encuentran los archivos .parquet.

    Returns:
        dict: Un diccionario con los nombres base de los archivos (sin extensión)
              como claves y los DataFrames correspondientes como valores.
              Además, crea variables globales del tipo df_<nombre> para fácil acceso.
    """
    try:
        dataframes = {}
        archivos = [f for f in os.listdir(carpeta) if f.endswith(".parquet")]

        if not archivos:
            print("No se encontraron archivos Parquet en la carpeta especificada.")
            return None

        for archivo in archivos:
            nombre_base = os.path.splitext(archivo)[0].lower().replace(" ", "_")
            ruta = os.path.join(carpeta, archivo)

            df = pd.read_parquet(ruta)
            dataframes[nombre_base] = df


        return dataframes

    except Exception as e:
        print(f"Error al cargar los archivos Parquet: {e}")
        return None
    


def generar_tabla_goles(df_partido_liga_temp:pd.DataFrame):

    """
    Lee el DataFrame de Partidos-Liga-Temporada.

    Args:
        df: DataFrame de Partidos-Liga-Temporada Gold.

    Returns:
        df: Un Dataframe con la tabla de Goles por equipo y temporada.
    """
    # Crear DataFrame con goles de local
    goles_local = (
        df_partido_liga_temp[['temporada', 'liga', 'local', 'goles_local', 'goles_visitante']]
        .rename(columns={
            'local': 'equipo',
            'goles_local': 'goles_hechos_local',
            'goles_visitante': 'goles_recibidos_local'
        })
    )

    # Crear DataFrame con goles de visitante
    goles_visitante = (
        df_partido_liga_temp[['temporada', 'liga', 'visitante', 'goles_local', 'goles_visitante']]
        .rename(columns={
            'visitante': 'equipo',
            'goles_visitante': 'goles_hechos_visitante',
            'goles_local': 'goles_recibidos_visitante'
        })
    )

    # Unir ambos roles (local y visitante)
    goles_equipo = pd.concat([goles_local, goles_visitante], ignore_index=True)

    # Agrupar para obtener los totales
    df_goles_equipo = (
        goles_equipo
        .groupby(['temporada', 'liga', 'equipo'], as_index=False)
        .agg({
            'goles_hechos_local': 'sum',
            'goles_recibidos_local': 'sum',
            'goles_hechos_visitante': 'sum',
            'goles_recibidos_visitante': 'sum'
        })
    )

    # Calcular métricas totales
    df_goles_equipo['goles_a_favor'] = df_goles_equipo['goles_hechos_local'] + df_goles_equipo['goles_hechos_visitante']
    df_goles_equipo['goles_en_contra'] = df_goles_equipo['goles_recibidos_local'] + df_goles_equipo['goles_recibidos_visitante']
    df_goles_equipo['diferencia_goles'] = df_goles_equipo['goles_a_favor'] - df_goles_equipo['goles_en_contra']

    # Reordenar columnas para legibilidad
    df_goles_equipo = df_goles_equipo[
        ['temporada', 'liga', 'equipo',
        'goles_hechos_local', 'goles_hechos_visitante',
        'goles_a_favor', 'goles_recibidos_local', 'goles_recibidos_visitante',
        'goles_en_contra', 'diferencia_goles']
    ].sort_values(['temporada', 'liga', 'goles_a_favor'], ascending=[True, True, False])

    return df_goles_equipo