# Sistema de recomendación de música de Spotify 🎵

Sistema de recomendación musical desarrollado en Python que combina características acústicas de Spotify y similitud de géneros para identificar canciones con características musicales similares. El proyecto utiliza técnicas de análisis de datos, procesamiento de características y aprendizaje automático no supervisado para construir un recomendador híbrido basado en similitud.

## Objetivo

Desarrollar un sistema capaz de recomendar canciones a partir de una canción de referencia, considerando tanto sus características acústicas como su información de género. El propósito es explorar cómo combinar diferentes criterios de similitud para generar recomendaciones relevantes a partir de un catálogo musical extenso.

## Dataset

Se utilizó el conjunto de datos **Spotify Tracks Dataset**, obtenido de Kaggle. El catálogo original contiene aproximadamente 114,000 registros e información sobre canciones, artistas, géneros y características musicales. Después del proceso de limpieza se obtuvo un catálogo de **89,578 canciones**, sin registros duplicados ni valores faltantes.

Para el sistema de recomendación se seleccionaron nueve características acústicas:

* Danceability
* Energy
* Loudness
* Speechiness
* Acousticness
* Instrumentalness
* Liveness
* Valence
* Tempo

Estas variables fueron estandarizadas mediante `StandardScaler` para facilitar su utilización en los cálculos de distancia y similitud.

## Proceso de desarrollo

El proyecto se organizó en siete etapas:

1. **Preparación del entorno:** configuración de Python, instalación de dependencias y organización de la estructura del proyecto.
2. **Limpieza de datos:** tratamiento de valores faltantes, registros duplicados e identificadores repetidos.
3. **Análisis exploratorio:** estudio de la distribución de popularidad, géneros musicales y relaciones entre variables acústicas.
4. **Preparación de variables:** selección de características musicales y estandarización mediante `StandardScaler`.
5. **Recomendador inicial:** implementación de un modelo basado en similitud coseno.
6. **Recomendador híbrido:** integración de filtros por género, distancia euclidiana y similitud coseno.
7. **Evaluación:** análisis de la consistencia de las recomendaciones, diversidad de artistas, distribución de popularidad y limitaciones del modelo.

## Sistema de recomendación

El recomendador híbrido utiliza dos criterios complementarios:

- **Filtrado por género:** selecciona canciones que comparten al menos un género con la canción de referencia.
- **Similitud acústica:** utiliza la distancia euclidiana para seleccionar candidatos y la similitud coseno para establecer el orden final de las recomendaciones.

El sistema también elimina canciones equivalentes a la referencia y evita recomendar múltiples registros de una misma combinación de título y artista. El resultado es una lista de canciones ordenadas por similitud, acompañadas de información sobre sus artistas, géneros, álbumes y puntuaciones calculadas.

## Principales resultados y limitaciones

- Se construyó un catálogo depurado de 89,578 canciones.
- El sistema utiliza nueve características acústicas estandarizadas y un filtro basado en géneros musicales.
- Se implementó un proceso híbrido de selección y ordenamiento de candidatos.
- Las pruebas realizadas permitieron examinar la consistencia de las recomendaciones, la diversidad de artistas y su distribución de popularidad.

**Limitaciones:** el conjunto de datos no contiene valoraciones personales ni historial de escucha de usuarios. Por ello, no es posible medir directamente la satisfacción de los usuarios ni validar las recomendaciones frente a preferencias individuales. La evaluación se centró en criterios internos de consistencia y características de los resultados.

## Herramientas

- **Python:** lenguaje principal.
- **Pandas y NumPy:** manipulación y procesamiento de datos.
- **Matplotlib y Seaborn:** análisis exploratorio y visualización.
- **Scikit-learn:** estandarización y métricas de similitud.
- **Jupyter Notebook:** desarrollo y experimentación.
- **Git y GitHub:** control de versiones y publicación del proyecto.

## Archivos

* `data/`: conjuntos de datos original, limpio y estandarizado utilizados durante el desarrollo del proyecto.
* `notebooks/`: notebooks de Jupyter correspondientes a las siete etapas de desarrollo, desde la exploración inicial hasta la evaluación del recomendador.
* `src/`: módulos de Python con las funciones para cargar los datos y ejecutar el sistema de recomendación.
* `documentation/`: documentación completa del proyecto, incluyendo las decisiones metodológicas y los principales resultados.
* `requirements.txt`: dependencias de Python necesarias para ejecutar el proyecto.
* `.gitignore`: archivos y directorios excluidos del control de versiones.

## Documentación

La documentación del proyecto incluye una descripción de las siete etapas de desarrollo, las decisiones metodológicas y los principales resultados. Consulte el documento completo en [`documentation/project_documentation.pdf`](documentation/project_documentation.pdf).

## Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/danielrfrancisco/spotify-music-recommender.git
cd spotify-music-recommender
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Abrir Jupyter Notebook:

```bash
jupyter notebook
```

5. Ejecutar los notebooks en orden, desde el análisis inicial hasta la evaluación del recomendador.

Para probar el sistema, se puede ejecutar el recomendador híbrido desde el notebook correspondiente.

## Fuente de datos

Saichaitanya Reddy, [Spotify Tracks Dataset - Audio Features](https://www.kaggle.com/datasets/saichaitanyareddyai/spotify-tracks-dataset-audio-features), Kaggle. Los archivos originales y procesados se incluyen en el repositorio para facilitar la reproducibilidad del proyecto.
