from fastapi import FastAPI, Query
from reccs import AnimeRecomendacion
import pandas as pd
import os

DIRECTORIO_RATINGS = r".\rating_limpiado.csv"
DIRECTORIO_ANIME = r".\anime.csv"

app = FastAPI(title="Anime Recommendation API")

recomendacion = AnimeRecomendacion(DIRECTORIO_RATINGS, DIRECTORIO_ANIME)

@app.get("/recommendations")
def get_recommendations(anime: str = Query(...), rating: float = Query(5.0)):
    recs = recomendacion.get_recommendations(anime, rating)
    if recs is None or recs.empty:
        return {"error": f"No se han encontrado recomendaciones para '{anime}'."}
    return recs.to_dict(orient="records")

@app.post("/update")
def update_correlation(force: bool = Query(False)):
    """
    Recompute the correlation matrix using the ratings file.
    If force=False, only compute if the .pkl file does not exist.
    """
    if not force and os.path.exists(recomendacion.cache_file):
        return {"message": "Correlation matrix already exists, skipping update."}

    ratings_df = pd.read_csv(DIRECTORIO_RATINGS)
    recomendacion.update_correlation(ratings_df)
    return {"message": "Correlation matrix updated successfully."}
