import pandas as pd
import numpy as np

df = pd.read_csv('netflix_titles.csv')
df.head()
df.rename(columns={'type': 'tipo', 'title': 'titulo','cast': 'reparto','country': 'pais','date_added': 'fecha_de_agregado','release_year': 'anio_de_lanzamiento','rating': 'valoracion','duration': 'duracion','listed_in': 'genero','description': 'descripcion'}, inplace=True)
df.rename(columns={'valoracion': 'clasificacion'}, inplace=True)
df['fecha_de_agregado'] = pd.to_datetime(df['fecha_de_agregado'], errors='coerce')
df['director'].fillna('Desconocido', inplace=True)
df['reparto'].fillna('Desconocido', inplace=True)
df['pais'].fillna('Desconocido', inplace=True)
df['fecha_de_agregado'].fillna(df['anio_de_lanzamiento'].astype(str) + "-01-01", inplace=True)
df['clasificacion'].fillna('Desconocido', inplace=True)
df['duracion'].fillna('Desconocido', inplace=True)
netflix_peliculas = pd.read_csv('netflix_peliculas.csv')
nxp= netflix_peliculas
nxs = pd.read_csv('netflix_series.csv')
nxs = netflix_series = pd.read_csv('netflix_series.csv')
nxp['fecha_de_agregado'] = pd.to_datetime(nxp['fecha_de_agregado'], errors='coerce')
nxs['fecha_de_agregado'] = pd.to_datetime(nxs['fecha_de_agregado'], errors='coerce')
nxp['duracion_num'] = nxp['duracion'].str.extract(r'(\d+)').astype(float)
nxp['duracion_unit'] = nxp['duracion'].str.extract(r'([A-Za-z ]+)$')
nxs['duracion_num'] = nxs['duracion'].str.extract(r'(\d+)').astype(float)
nxs['duracion_unit'] = nxs['duracion'].str.extract(r'([A-Za-z ]+)$')
df['reparto'] = df['reparto'].str.lower()
df['director'] = df['director'].str.lower()
df['titulo'] = df['titulo'].str.lower()
df['pais'] = df['pais'].str.lower()
df['genero'] = df['genero'].str.lower()
df['descripcion'] = df['descripcion'].str.lower()
df['clasificacion'] = df['clasificacion'].str.lower()
df['tipo'] = df['tipo'].str.lower()
df['genero'].replace('TV', '', regex=True, inplace=True)
df['genero'] = df['genero'].str.strip()

def buscar_por_actor_o_director(nombre):
    nombre = nombre.lower()
    return df.loc[(df['reparto'].str.contains(nombre, na=False)) | (df['director'].str.contains(nombre, na=False)), ['titulo', 'tipo', 'director', 'reparto']]

def peliculas_al_azar(n):
    return df.sample(n)

def buscar_por_genero(elegenero):
    genero = elegenero.lower()
    return df.loc[(df['genero'].str.contains(genero, na=False)), ['titulo', 'tipo', 'director', 'reparto']]

tiempo_total = (nxp['duracion_num'].sum() / 60)/24

tiempo_total_series = (nxs['duracion_num'].sum()*20/24)

duracion_estandar_series = nxs['duracion_num'].values * 1200
def estadisticas_anios(año):
    año = int(año)
    peliculas_año = nxp[nxp['anio_de_lanzamiento'] == año]
    series_año = nxs[nxs['anio_de_lanzamiento'] == año]
    duracion_peliculas = peliculas_año['duracion_num'].mean()
    minima_duracion = peliculas_año['duracion_num'].min()
    maxima_duracion = peliculas_año['duracion_num'].max()
    duracion_series = duracion_estandar_series.mean()
    minima_duracion_series = duracion_estandar_series.min()
    maxima_duracion_series = duracion_estandar_series.max()
    if año not in nxp['anio_de_lanzamiento'].values and año not in nxs['anio_de_lanzamiento'].values:
        print(f"No hay datos disponibles para el año {año}.")
        return
    else:
        print(f"En el año {año}, la duración promedio de las peliculas fue de {duracion_peliculas:.2f} minutos, la minima duración fue de {minima_duracion} minutos y la máxima duración fue de {maxima_duracion} minutos.")
        print(f"En el año {año}, la duración promedio de las series fue de {duracion_series:.2f} minutos, la minima duración fue de {minima_duracion_series} minutos y la máxima duración fue de {maxima_duracion_series} minutos.")
        print(f"En el año {año}, se lanzaron {peliculas_año.shape[0]} peliculas y {series_año.shape[0]} series.")
    return

def recomendaciones_por_duracion(duracion):
    duracion = float(duracion)
    peliculas_similares = nxp[(nxp['duracion_num'] >= duracion) & (nxp['duracion_num'] <= duracion)].head(1)
    return peliculas_similares[['titulo', 'duracion_num', 'director', 'reparto']]

def menu():
    print("Bienvenido al sistema de recomendaciones de Netflix")
    print("1. Buscar por actor o director")
    print("2. Buscar por género")
    print("3. Obtener película al azar")
    print("4. Estadísticas por año")
    print("5. Recomendaciones por duración")
    print("6. Salir")
    
    while True:
        choice = input("Seleccione una opción (1-6): ")
        
        if choice == '1':
            nombre = input("Ingrese actor o director: ")
            resultados = buscar_por_actor_o_director(nombre)
            print(resultados)
        elif choice == '2':
            genero = input("Ingrese el género: ")
            resultados = buscar_por_genero(genero)
            print(resultados)
        elif choice == '3':
            azar = peliculas_al_azar(1)
            print(azar) 
        elif choice == '4':
            año = int(input("Ingrese el año que desea consultar: "))
            estadisticas_anios(año)
        elif choice == '5':
            duracion = int(input("Ingrese la duración en minutos: "))
            resultados = recomendaciones_por_duracion(duracion)
            print(resultados)
        elif choice == '6':
            print("Gracias por usar el sistema de recomendaciones de Netflix. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 6.")

menu()
