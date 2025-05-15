# conteo_periodo.py

import pandas as pd

def contar_por_anio_trimestre_o_mes(df, periodo="trimestre"):
       
    # Verificar si las columnas necesarias están en el DataFrame
    if 'anio' not in df.columns or ('trimestre' not in df.columns and 'mes' not in df.columns):
        raise ValueError("El DataFrame debe contener las columnas 'anio', 'trimestre' y/o 'mes'")
    
    # Agrupar por 'anio', 'anio y trimestre' o 'anio y mes'
    if periodo == "anio":
        conteo = df.groupby(['anio']).size().reset_index(name="conteo")
    elif periodo == "trimestre":
        conteo = df.groupby(['anio', 'trimestre']).size().reset_index(name="conteo")
    elif periodo == "mes":
        conteo = df.groupby(['anio', 'mes']).size().reset_index(name="conteo")
    else:
        raise ValueError("El parámetro 'periodo' debe ser 'anio', 'trimestre' o 'mes'")

    return conteo