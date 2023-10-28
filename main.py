from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import jinja2
import pandas as pd
#import ast
#from pydantic import BaseModel

# --------------------- Leyendo y cargando los archivos csv ----------------------------------------
f_playtimegenre1 = 'data//genre_playtime.csv'
f_userforgenre2 = 'data//jugador_masminutos.csv'
f_usersrecommend3 = 'data//top_reviews3.csv'
f_usernotrecommend4 = 'data//top_reviews4.csv'
f_sentiment5 = 'data//SentimientoxAño.csv'





path = "https://raw.githubusercontent.com/AlexdeAlba/Henry-Proyect1/main/"

# Carga el DataFrame desde un archivo CSV y selecciona solo las columnas especificadas
columns_to_keep = ['budget', 'id','revenue','title','vote_average','vote_count','release_date','release_year','return']
#df = pd.read_csv(url, usecols=columns_to_keep)

#Lee Movie_clean
fileName = "movies_clean.csv"
df = pd.read_csv(path + fileName)
# Convertir la columna 'release_date' a formato datetime
df['release_date'] = pd.to_datetime(df['release_date'])


#Lee cast 
fileName = "cast.csv"
df_cast = pd.read_csv(path + fileName)
#convertir id en entero y cast a diccionarios
df_cast['id'] = df_cast['id'].astype(int)
df_cast['cast'] = df_cast['cast'].apply(ast.literal_eval)

#Lee crew
fileName = "crew.csv"
df_crew = pd.read_csv(path + fileName)
#convertir id en entero y crew a diccionarios
df_crew['id'] = df_crew['id'].astype(int)
df_crew['crew'] = df_crew['crew'].apply(ast.literal_eval)

# --------------------------- Manejo de Memoria --------------------------------------------




# ------------------------- Declaracion de la clase movie ------------------------------------




    #-----------------------------------------------
    #  1.   Cantidad de filamaciones de un mes  
    #-----------------------------------------------  
    def cantidad_filmaciones_mes(self,mes):
        mes_ingles = self.get_mes(mes)
        if mes_ingles is None:
            return 'Mes no válido'
        # Filtrar los registros que correspondan al mes ingresado
        mask = df['release_date'].dt.month == pd.to_datetime(mes_ingles, format='%B').month
        peliculas_mes = df.loc[mask]
        # Obtener la cantidad de películas en el mes
        cantidad_peliculas_mes = len(peliculas_mes)
        return cantidad_peliculas_mes

    #-----------------------------------------------
    # 2. Cantidad de filmaciones en un dia de semana 
    # (Lunes, Martes, Miercoles etc)
    #-----------------------------------------------
    def cantidad_filmaciones_dia(self, dia):
        dia_semana = self.get_diaSemana(dia)
        print(dia_semana)
        peliculas_estreno = df[df['release_date'].dt.weekday == dia_semana]
        return peliculas_estreno.shape[0]    
    
    #-----------------------------------------------
    # 3. Retorna el título, el año de estreno y el score 
    #-----------------------------------------------
    def score_titulo(self, titulo):
        titulo_low = titulo.lower()
        movie = df.loc[df['title'] == titulo_low]
        lista = movie[['title', 'release_year', 'popularity']].values.tolist()[0]
        return lista
        
        
    #-----------------------------------------------
    # 4. Retorna Cantidad d votos  y el valor promedio
    #    de las votaciones 
    #-----------------------------------------------
    def votos_titulo(self,titulo):
        # Filtrar el DataFrame por el título buscado
        titulo_low = titulo.lower()
        pelicula = df[df['title'] == titulo_low]
        # Si lo encuentra
        if not pelicula.empty: 
            #peli = pelicula['title'].iloc[0]
            peli = titulo #Uso titulo para que salga igual al del usuario
            year = pelicula['release_year'].iloc[0]   
            votos = pelicula['vote_count'].iloc[0]
            score = pelicula['vote_average'].iloc[0] 
            listaReturn = [peli,year,votos,score]
            return listaReturn
        else:
            return None 
        #f"No se encontro el titulo buscado: {titulo_low}"
    
    #-----------------------------------------------
    # 5. Retorna el exito de un actor medido con el retorno
    #    ademas cantidad de peliculas y promedio de retorno
    #-----------------------------------------------
    def get_actor(self, nombre_actor):
        ids_peliculas = []
        #df_cast = read_cast()
        for index, row in df_cast.iterrows():
            actores = row['cast']
            for actor in actores:
                if actor['name'] == nombre_actor:
                    ids_peliculas.append(row['id'])

        # Seleccionamos los ids de la lista
        df_res= df[df['id'].isin(ids_peliculas)]
        #Numero de peliculas del actor
        numFilms = df_res.shape[0]
        # Suma de Ganancias por las peliculas
        ganancia = df_res['return'].sum()
        # Promedio por pelicula
        promedio = ganancia/numFilms

        lista = [numFilms,ganancia,promedio] 
        #del df_cast        
        return lista
    
  
    #-----------------------------------------------
    # 6.Retorna el exito de un director medido con el retorno
    #    ademas nombre de cada pelicula, fecha de lanzamiento
    #    costo, ganancia y retorno por pelicula 
    #-----------------------------------------------   
    def get_director(self, nombre_director):
        ids_peliculas = []
        #df_crew = read_crew()
        for index, row in df_crew.iterrows():
            directores = row['crew']
            for director in directores:
                if director['name'] == nombre_director and director["job"] == "Director":
                    ids_peliculas.append(row['id'])

        numPeliculas = len(ids_peliculas)
        # Seleccionamos los ids de la lista
        df_res= df[df['id'].isin(ids_peliculas)]
        columnas = ['title','release_date','revenue','budget','return']
        df_return = df_res.loc[:,columnas]

        if numPeliculas <= 0:
            ganancia = 0
            promedio = 0
        else:
            ganancia = df_res['return'].sum()
            promedio = ganancia/numPeliculas
        #del df_crew
        return df_return, nombre_director, ganancia, promedio
    

    #--------------Complementarias----------------- 
    #Retona el mes en ingles
    def get_mes(self, mes):
        return self.meses.get(mes.lower())
    
    #Retorna el dia de la semana en entero
    # Lunes = 0, etc
    def get_diaSemana(self,dia):
        dia_sem = dia.lower()
        return self.diaSemana.get(dia_sem)
    
    
        


#Instanciando la clase
movi = movie()

# -----------------------------Funciones para FastAPI -----------------------------------------


# Crear una instancia de la aplicación FastAPI
app = FastAPI()

@app.get("/")
def inicio():
  return "Proyecto Henry (Movies)"

# 1.-------------------------------------------------------------
@app.get("/PlayTimeGenre/{genero}")
def cantidad_filmaciones_mes(mes=None):
  cantidad = movi.cantidad_filmaciones_mes(mes)
  return f"cantidad de filmaciones en el mes de {mes}: {cantidad}"

# 2.-------------------------------------------------------------
@app.get("/UserForGenre/{genero}")
def cantidad_filmaciones_dia(dia=None):
    cant = movi.cantidad_filmaciones_dia(dia)
    return f"Numero de peliculas estrenadas en {dia}: {cant}"

# 3.-------------------------------------------------------------
# Retorna el título, el año de estreno y el score
@app.get("/UsersRecommend/{año}")
def score_titulo( titulo_de_la_filmacion ):
    resp = movi.score_titulo(titulo_de_la_filmacion)
    return f"La Pelicula {titulo_de_la_filmacion} se estreno en {resp[1]} con un score de {resp[2]}"

# 4.-------------------------------------------------------------
@app.get("/UsersNotRecommend/{año}")
def votos_titulo(titulo):
    res = movi.votos_titulo(titulo)
    if res == None:
        return f"No se encontraron datos de la pelicula {titulo}"
    else:
        return f"La pelicula {res[0]} fue estrenada en {res[1]} con {res[2]} votos y un score de {res[3]}"

# 5.-------------------------------------------------------------
@app.get("/sentiment_analysis/{nombre_actor}")
def get_actor(actor):
    res = movi.get_actor(actor)
    return f"{actor} a realizado {res[0]} filmaciones con un total de ganancias de $ {res[1]:,.2f} y un promedio de $ {res[2]:,.2f} por pelicula"

# 6.-------------------------------------------------------------
@app.get("/recomendacion/{juego}")
def recomienda(juego):
s


# ---------------------  Inicia el servidor con uvicorn -----------------------------

# Iniciar el servidor de desarrollo con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    