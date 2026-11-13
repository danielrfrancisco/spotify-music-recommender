
from pathlib import Path
import pandas as pd


# Directorio raíz del proyecto
DIRECTORIO_PROYECTO = Path(__file__).resolve().parent.parent

# Rutas de los archivos
RUTA_CATALOGO = DIRECTORIO_PROYECTO / 'data' / 'spotify-tracks-dataset-clean.csv'
RUTA_CARACTERISTICAS = DIRECTORIO_PROYECTO / 'data' / 'spotify-audio-features-scaled.csv'


def cargar_datos():
    """
    Carga el catálogo de canciones y la matriz de características escaladas.

    Construye la columna genres_set y verifica que ambos conjuntos de datos conserven los mismos índices.

    Devuelve:
        df: catálogo de canciones.
        X_audio_scaled: matriz de características acústicas estandarizadas.
    """

    # Cargar los archivos
    df = pd.read_csv(RUTA_CATALOGO)
    X_audio_scaled = pd.read_csv(RUTA_CARACTERISTICAS, index_col = 0)

    # Verificar que ambos conjuntos tengan los mismos índices
    if not df.index.equals(X_audio_scaled.index):
        raise ValueError(
            'Los índices del catálogo y de la matriz escalada no coinciden.'
        )

    # Verificar que existan las etiquetas de género
    if df['track_genre'].isna().any():
        raise ValueError(
            'El catálogo contiene canciones sin información de género.'
        )

    # Separar los géneros y almacenarlos como conjuntos
    df['genres_set'] = df['track_genre'].apply(
        lambda x: set(x.split(';'))
    )

    return df, X_audio_scaled