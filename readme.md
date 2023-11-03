#### Proyecto individual Henry (Steam Games)
# Sistema de Recomendación de Videojuegos para Usuarios en Steam

## Descripción del Problema

### Contexto
Este primer trabajo se presenta como un un conjunto de proyectospara terminar el bootcamp de Data Sicnce en Henry. Estos serán 3 proyectos, de los cuales 2 seran individuales y el tercero en equipo

Este proyecto se enfoca en la solucion de 5 consultas como primera parte del mismo, cada una con su funcion corespondiente  resolviendo la consulta solicitada.
   - Año con más horas jugadas de un genero dado
   - Usuario que acomula mayor numero de horas jugadas en un genero dado acompañado de una lista de horas jugadas por año
   - Los 3 juegos más recomendados por usuarios para un año dado
   - Los 3 juegos menos recomendados por los usuarios para un año dado
     De acuerdo a un analisis de sentimiento presentar una lista de cantidad de reseñas por un año dado, presentando estas cantidades en 3 grupos: Positivas, neutra y negativas.
     
Como segunda parte de este proyecto se ha realizado un sistema de recomendacion de juegos de acuerdo a un juego proporcionado por el usuario. Para este análisis   sa ha utilizado  el nmetodo de **Similitud del Coseno**    basandonos en la biblioteca de Scikit-learn.

Este proyecto es presentando en una API a la cual se podrá accesar por medio de la plataforma **[render.com](https://proyecto-01-henry.onrender.com/docs)**. Tambien se incluye un video para mostrar el resultado de las consultas propuestas y del modelo ML entrenado **[Vide del proyecto Steam](http://linkgoogle.com)**

### Propuesta de Trabajo

El trabajo se divide en las siguientes etapas:

### 1. Transformaciones de Datos
 
 Las 3 bases de datos que se proporcionaron para realizar el proyecto se presentaron en un formato JSON (australian_user_reviews.json,  australian_users_items.json y output_steam_games.json) se decidio trabajar con ellas transformandolas en archivos csv, por facilidad mia del manejo de los datos, aunque estoy consiente que los archivos JSON son muy eficientes para poder trabajar con ellos.
 
 Como primer paso en el archivo **01-Files_to_CSV** se conviertieron los 3 archivos a csv.
 

 |Archivo Origen|Archivo Final|
  |---|---|
 | output_steam_games.json|Steam-Games.csv|
 |australian_user_reviews.json|Reviews.csv|
 |australian_users_items.json|Items.csv|
 
### 2. Exploración de datos. EDA (Exploratory Data Analysis) 
 En este paso se verificara cada una de las bases de datos considerando:
 * Consideraciones
  *  Valores nulos
  *  Valores atípicos (outliers)
  *  Valores duplicados
  *  Codificación de datos categóricos
  *  Consistencia de datos
  *  Tratamiento de datos erróneos
 
 
### 3. Feature Engineering
Se debe crear una columna llamada 'sentiment_analysis' en el dataset 'user_reviews'. Esta columna aplicará análisis de sentimiento con NLP y utilizará una escala que asigna:
- '0' si la reseña es mala.
- '1' si la reseña es neutral.
- '2' si la reseña es positiva.

La nueva columna reemplazará la columna 'user_reviews.review' para facilitar el trabajo de los modelos de machine learning.

### 4. Desarrollo de la API
Se propone disponibilizar los datos utilizando el framework FastAPI. La API contendrá las siguientes consultas:

#### Consulta 1: PlayTimeGenre
```python
@app.get('/play-time-genre/{genero}')
# Devuelve el año con más horas jugadas para el género dado.
```

#### Consulta 2: UserForGenre
```python
@app.get('/user-for-genre/{genero}')
# Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
```

#### Consulta 3: UsersRecommend
```python
@app.get('/users-recommend/{año}')
# Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
```

#### Consulta 4: UsersNotRecommend
```python
@app.get('/users-not-recommend/{año}')
# Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.
```

#### Consulta 5: SentimentAnalysis
```python
@app.get('/sentiment-analysis/{año}')
# Según el año de lanzamiento, devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados con un análisis de sentimiento.
```

### 5. Deployment
La API debe será desplegada para ser accesible desde cualquier dispositivo conectado a internet 
**[render.com](https://proyecto-01-henry.onrender.com/docs)**
### 6. Análisis Exploratorio de los Datos (EDA)
Después de limpiar los datos, se llevará a cabo un análisis exploratorio para investigar relaciones entre variables, identificar outliers y buscar patrones interesantes.

### 7. Modelo de Aprendizaje Automático
Se entreno un modelo de machine learning para desarrollar un sistema de recomendación  ítem-ítem o 

#### Consulta: Recomendación de Juego
```python
@app.get('/recomendacion-juego/{id_de_producto}')
# Ingresando el id de producto, recibir una lista con 5 juegos recomendados similares al ingresado.
```

### 8. Video
Video de presentación de utilización de la herramienta el link se proprcionara



