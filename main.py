from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from fastapi.responses import PlainTextResponse

import jinja2
import pandas as pd
import gdown
#import ast
#from pydantic import BaseModel

# --------------------- Leyendo y cargando los archivos csv ----------------------------------------

f_playtimegenre1 = 'data//genre_playtime.csv'
df1 = pd.read_csv(f_playtimegenre1)
f_userforgenre2 = 'data//jugador_masminutos.csv'
df2 = pd.read_csv(f_userforgenre2)
f_usersrecommend3 = 'data//top_reviews3.csv'
df3 = pd.read_csv(f_usersrecommend3)
f_usernotrecommend4 = 'data//top_reviews4.csv'
df4 = pd.read_csv(f_usernotrecommend4)
f_sentiment5 = 'data//SentimientoxAño.csv'
df5 = pd.read_csv(f_sentiment5)
f_recommend6 = 'data//Recommend.csv '
#df6 = pd.read_csv(f_recommend6)

f_playtimegenre1 = '1-jSl5Hk6j2xtFuW9i0-GJ527w1mrXpgN'
f_userforgenre2 = '1-k4MrmQRoBnm34_Ys-AhjjCWxXh7adda'
f_usersrecommend3 = '1-mKrWZRWlqVDB0DVeI2Ko4ZxxwAsLkdH'
f_usernotrecommend4 = '1-l77tYd5A59wz4V-39iwzoPT0GCAvnSe'
f_sentiment5 = '1-oeNsO3GTYS9ShAPqRFvqxUEHspBIzPK'
f_recomend6 = ' '

""" 
# Enlace de descarga directa del archivo CSV
file_url = "https://drive.google.com/uc?id=" + f_playtimegenre1
gdown.download(file_url, 'genre_playtime.csv', quiet=False)

file_url = "https://drive.google.com/uc?id=" + f_userforgenre2
gdown.download(file_url, 'jugador_masminutos.csv', quiet=False)

file_url = "https://drive.google.com/uc?id=" + f_usersrecommend3
gdown.download(file_url, 'top_reviews3.csv', quiet=False)

file_url = "https://drive.google.com/uc?id=" + f_usernotrecommend4
gdown.download(file_url, 'top_reviews4.csv', quiet=False)

file_url = "https://drive.google.com/uc?id=" + f_sentiment5
gdown.download(file_url, 'SentimientoxAño.csv', quiet=False)

file_url = "https://drive.google.com/uc?id=" + f_recomend6
gdown.download(file_url, 'top_reviews3.csv', quiet=False)
"""


# --------------------------- Manejo de Memoria --------------------------------------------
# ------------------------- Declaracion de la clase movie ------------------------------------
# -----------------------------Funciones para FastAPI -----------------------------------------


# Crear una instancia de la aplicación FastAPI
app = FastAPI()

@app.get("/")
def inicio():
    return "Proyecto Henry (Movies)"

# ---------------------------------------------------------------
# 1.-------------------------------------------------------------
@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero):
    # Leer el archivo CSV con Pandas
    df1 = pd.read_csv('genre_playtime.csv')
    # Cambio a minúsculas
    genero = genero.lower()
    filtro = df1[df1['genres'] == genero]
    
    if filtro.empty:
        return -1
    else:
        year = filtro.loc[filtro['hrs_jugadas'].idxmax()]['year']
        
    if year != -1:
         respuesta = f'Año de lanzamiento con más horas jugadas para el género {genero} : {year}'
    else:
        respuesta = f"No existen registros para el género '{genero}'"
    del df1    

    return respuesta

# ---------------------------------------------------------------
# 2.-------------------------------------------------------------
# Configura las plantillas de Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/UserForGenre/{genero}", response_class=HTMLResponse)
def UserForGenre(genero:str,request:Request):
    # Leer el archivo CSV con Pandas
    df2 = pd.read_csv('jugador_masminutos.csv')
    gen = genero.capitalize()
    genero = genero.lower()
    # Filtrar las filas que corresponden al género dado
    filtro = df2[df2['genres'] == genero]
    total = 0
    if filtro.empty:
        return templates.TemplateResponse("resultado.html", {"request": request, "usuario_max_horas": "No hay registros para el género dado", "acumulacion_horas": [], "genero": genero})

    # Encontrar al usuario con más horas jugadas
    usuario_max_horas = filtro.loc[filtro['total_min'].idxmax()]['user_id']
    usuario_max_horas = usuario_max_horas.upper()
    # Crear una lista de acumulación de horas jugadas por año
    acumulacion_horas = []
    for año, grupo in filtro.groupby('year'):
        horas_año = grupo['min_jugados'].sum()
        total = total + horas_año
        acumulacion_horas.append((año, horas_año))

    # Renderiza el resultado utilizando la plantilla HTML
    return templates.TemplateResponse("ask2.html", {"request": request, "usuario": usuario_max_horas, "acumulacion": acumulacion_horas, "genero": gen,"total":total})

# ---------------------------------------------------------------
# 3.-------------------------------------------------------------


@app.get("/UsersRecommend/{anio}")
def UsersRecommend(anio:int):
    # Leer el archivo CSV con Pandas
    df3 = pd.read_csv('top_reviews3.csv')
    
    # Filtrar las filas que corresponden al año dado
    filtro = df3[df3['year'] == anio]
    # filtro = pd.DataFrame() #Declara el df empty
    res = ""

    if filtro.empty:
        return  f"No hay registros para el año dado"

    # Ordenar las filas por la columna 'total_review' de manera descendente
    filtro = filtro.sort_values(by='total_review', ascending=False)
    
    # Tomar las tres primeras filas como los juegos más recomendados
    top_3_juegos = filtro.head(3)
    
    # Crear el resultado en una lista de diccionarios
    resultado = []

    for i, (_, juego) in enumerate(top_3_juegos.iterrows(), start=1):
        resultado.append({f'Puesto {i}': juego['title']})
        res += f"Puesto {i}.- {juego['title']}\n"
    
    return resultado
# ---------------------------------------------------------------
# 4.-------------------------------------------------------------
@app.get("/UsersNotRecommend/{anio}")
def UsersNotRecommend(anio:int):
    df4 = pd.read_csv('top_reviews4.csv')
    # Filtrar las filas que corresponden al año dado
    
    filtro = df4[df4['year'] == anio]
    
    if filtro.empty:
        return "No hay registros para el año dado"
    
    # Ordenar las filas por la columna 'false_recommend_count' de manera ascendente
    filtro = filtro.sort_values(by='false_recommend_count', ascending=True)
    res = ""

    # Tomar las tres primeras filas como los juegos menos recomendados
    top_3_juegos = filtro.head(3)
    
    # Crear el resultado en una lista de diccionarios
    resultado = []
    for i, (_, juego) in enumerate(top_3_juegos.iterrows(), start=1):
        resultado.append({f'Puesto {i}': juego['title']})
        res += f"Puesto {i}.- {juego['title']}\n"
    
    return resultado
# ---------------------------------------------------------------
# 5.-------------------------------------------------------------
@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis(anio:int):
    df5 = pd.read_csv('SentimientoxAño.csv')
    
    # Filtrar las filas que corresponden al año dado
    filtro = df5[df5['year'] == anio]
    
    if filtro.empty:
        return "No hay registros para el año dado"
    
    # Contar la cantidad de registros en cada categoría de sentimiento
    negativos = filtro['Negativo'].sum()
    neutrales = filtro['Neutral'].sum()
    positivos = filtro['Positivo'].sum()
    
    # Crear el resultado en un diccionario
    resultado = {'Negativos': negativos, 'Neutrales': neutrales, 'Positivos': positivos}
    res = f'Negativos: {negativos}, Neutrales: {neutrales}, Positivos: {positivos}'
    return res        
# ---------------------------------------------------------------

# 6.-------------------------------------------------------------

# ---------------------  Inicia el servidor con uvicorn -----------------------------
