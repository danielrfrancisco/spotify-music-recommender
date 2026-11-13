import pandas as pd
from IPython.display import display
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity

# Número máximo de coincidencias mostradas durante una búsqueda
LIMITE_RESULTADOS = 20

from src.datos import cargar_datos


# Cargar los datos del proyecto
df, X_audio_scaled = cargar_datos()

def buscar_cancion(nombre, artista = None):
    
    # Validar el nombre de la canción
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError('Debes proporcionar un nombre de canción válido.')

    # Validar el artista, si se proporciona
    if artista is not None and not isinstance(artista, str):
        raise TypeError('El artista debe ser una cadena de texto.')

    # Buscar coincidencias parciales en el título
    mascara = df['track_name'].str.contains(
        nombre.strip(),
        case = False,
        regex = False,
        na = False
    )

    # Filtrar también por artista, si se proporciona
    if artista is not None and artista.strip():
        mascara &= df['artists'].str.contains(
            artista.strip(),
            case = False,
            regex = False,
            na = False
        )

    # Obtener todos los resultados
    resultados = df.loc[
        mascara,
        ['track_name', 'artists', 'track_genre', 'album_name']
    ]

    return resultados

def seleccionar_cancion():
    
    while True:

        # Solicitar los datos de búsqueda
        nombre = input(
            'Introduce el nombre de la canción (o "salir" para terminar): '
        )

        # Comprobar si el usuario desea salir
        if nombre.strip().lower() in ['salir', 'exit']:
            print('Búsqueda finalizada.')
            return None

        # Comprobar que el nombre no esté vacío
        if not nombre.strip():
            print('Debes introducir el nombre de una canción.\n')
            continue

        artista = input('Introduce el artista (opcional): ')

        if artista.strip().lower() in ['salir', 'exit']:
            print('Búsqueda finalizada.')
            return None

        # Buscar coincidencias
        if artista.strip():
            coincidencias = buscar_cancion(nombre, artista)
        else:
            coincidencias = buscar_cancion(nombre)

        # Comprobar si existen coincidencias
        if coincidencias.empty:
            print('No se encontraron coincidencias.')
            print('Intenta realizar una nueva búsqueda.\n')
            continue

        # Si existe una sola coincidencia, obtener su índice
        if len(coincidencias) == 1:
            indice = coincidencias.index[0]

        # Si existen varias coincidencias, solicitar una selección
        else:

            # Comprobar si se supera el límite de resultados
            if len(coincidencias) > LIMITE_RESULTADOS:
                print(
                    f'\nSe encontraron más de {LIMITE_RESULTADOS} coincidencias. '
                    f'Mostrando las primeras {LIMITE_RESULTADOS} opciones.'
                )

            # Limitar las opciones mostradas
            opciones = coincidencias.head(LIMITE_RESULTADOS)

            print('\nCanciones encontradas:')
            display(opciones)

            print('\nIntroduce el índice de la canción que deseas seleccionar.')

            while True:
                entrada = input('Índice (o "salir" para cancelar): ').strip()

                if entrada.lower() in ['salir', 'exit']:
                    return None

                try:
                    indice = int(entrada)

                    if indice in opciones.index:
                        break
                    else:
                        print(
                            'El índice no corresponde a ninguna '
                            'de las opciones mostradas.'
                        )

                except ValueError:
                    print('Debes introducir un índice numérico.')

        # Mostrar la canción seleccionada
        print('\nCanción seleccionada:')
        display(df.loc[[indice], ['track_name', 'artists', 'album_name']])

        # Solicitar confirmación
        while True:
            respuesta = input(
                '¿Es esta la canción que buscabas? (sí/no): '
            ).strip().lower()

            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                print('\nCanción confirmada.')
                return indice

            elif respuesta in ['n', 'no']:
                print('\nVamos a realizar una nueva búsqueda.\n')
                break

            elif respuesta in ['salir', 'exit']:
                print('Búsqueda finalizada.')
                return None

            else:
                print('¡Respuesta no válida! Introduce "sí" o "no".')
                
def recomendar_canciones(indice, n_recomendaciones = 10):
    
    # Validar el índice de referencia
    if indice not in df.index:
        raise ValueError('El índice indicado no existe en el conjunto de datos.')

    # Validar el número de recomendaciones
    if not isinstance(n_recomendaciones, int) or isinstance(n_recomendaciones, bool):
        raise TypeError('El número de recomendaciones debe ser un entero.')

    if n_recomendaciones <= 0:
        raise ValueError('El número de recomendaciones debe ser positivo.')

    # Obtener los géneros de la canción de referencia
    generos_referencia = df.loc[indice, 'genres_set']

    # Filtrar canciones que compartan al menos un género
    mascara_genero = df['genres_set'].apply(
        lambda generos: bool(generos_referencia & generos)
    )

    # Excluir la canción de referencia y sus registros equivalentes
    referencia = df.loc[indice]

    misma_cancion = (
        (df['track_name'] == referencia['track_name']) &
        (df['artists'] == referencia['artists'])
    )

    mascara_genero = mascara_genero & ~misma_cancion
    candidatas = df.loc[mascara_genero].copy()

    # Obtener las características acústicas
    caracteristicas_referencia = X_audio_scaled.loc[[indice]]
    caracteristicas_candidatas = X_audio_scaled.loc[candidatas.index]

    # Calcular las distancias euclidianas
    distancias = euclidean_distances(
        caracteristicas_referencia,
        caracteristicas_candidatas
    ).flatten()

    distancias = pd.Series(distancias, index = candidatas.index)

    # Incorporar las distancias y eliminar canciones repetidas
    candidatas_unicas = (
        candidatas
        .assign(distancia_euclidiana = distancias)
        .sort_values(by = 'distancia_euclidiana', ascending = True)
        .drop_duplicates(subset = ['track_name', 'artists'], keep = 'first')
    )

    # Seleccionar las 100 canciones más cercanas
    candidatas_ordenadas = candidatas_unicas.sort_values(
        by = 'distancia_euclidiana',
        ascending = True
    )

    df_candidatas = candidatas_ordenadas.head(100).copy()

    indices_seleccionados = df_candidatas.index
    X_candidatas = X_audio_scaled.loc[indices_seleccionados]

    # Calcular la similitud del coseno
    similitudes = cosine_similarity(
        caracteristicas_referencia,
        X_candidatas
    ).flatten()

    similitudes = pd.Series(similitudes, index = X_candidatas.index)

    # Ordenar por similitud del coseno
    similitudes_ordenadas = similitudes.sort_values(ascending = False)

    # Construir la tabla de recomendaciones
    recomendaciones = df_candidatas.loc[
        similitudes_ordenadas.index,
        ['track_name', 'artists', 'track_genre', 'album_name']
    ].copy()

    recomendaciones['distancia_euclidiana'] = (
        df_candidatas.loc[recomendaciones.index, 'distancia_euclidiana']
    )

    recomendaciones['similitud_coseno'] = similitudes_ordenadas

    # Devolver las recomendaciones solicitadas
    return recomendaciones.head(n_recomendaciones)
                
def ejecutar_recomendador(n_recomendaciones = 10):
    
    # Solicitar la selección de una canción
    indice = seleccionar_cancion()

    # Comprobar si el usuario canceló la búsqueda
    if indice is None:
        return

    # Generar las recomendaciones
    recomendaciones = recomendar_canciones(
        indice,
        n_recomendaciones = n_recomendaciones
    )

    # Mostrar los resultados
    print('\nCanciones recomendadas:')
    display(recomendaciones)