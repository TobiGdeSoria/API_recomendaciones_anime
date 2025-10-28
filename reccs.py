import pandas as pd
import html
import time
import warnings

class AnimeRecomendacion:
    def __init__(self, directorio_ratings, directorio_anime):
        self.directorio_ratings = directorio_ratings
        self.directorio_anime = directorio_anime
        self.ratings = None
        self.animes = None
        self.corrMatrix = None
        self._load_data()

    def _load_data(self):
        print("Cargando base de datos... (Esto puede tardar un poco.)")
        r_cols = ['user_id', 'anime_id', 'rating']
        a_cols = ['anime_id', 'name']

        self.ratings = pd.read_csv(self.directorio_ratings, sep=',', names=r_cols, usecols=range(3),
                                   encoding="ISO-8859-1", skiprows=1, low_memory=False)
        self.animes = pd.read_csv(self.directorio_anime, sep=',', names=a_cols, usecols=range(2),
                                  encoding="ISO-8859-1", skiprows=1)
        self.animes['name'] = self.animes['name'].apply(html.unescape)

        userRatings = self.ratings.pivot_table(index='user_id', columns='anime_id', values='rating')
        anime_ids = userRatings.columns
        corr_matrix = pd.DataFrame(index=anime_ids, columns=anime_ids, dtype=float)

        warnings.filterwarnings("ignore", category=RuntimeWarning)

        start_time = time.time()
        total = len(anime_ids)

        bar_length = 40  # number of characters in the loading bar

        for i, col_i in enumerate(anime_ids, start=1):
            corr_matrix.loc[col_i, :] = userRatings.corrwith(userRatings[col_i], method='pearson')

             # Update progress bar every 10 columns or at the last column
            if i % 1 == 0 or i == total:
                elapsed = time.time() - start_time
                progress = i / total
                eta = (elapsed / i) * (total - i)

                filled_len = int(bar_length * progress)
                bar = '=' * filled_len + '-' * (bar_length - filled_len)

                print(f"\r[{bar}] {progress*100:5.1f}% - ETA: {eta:.2f}s", end='')

        print("\nAplicación preparada :D.")
        self.corrMatrix = corr_matrix

    def get_recommendations(self, anime_name, rating_value):
        anime_row = self.animes[self.animes['name'].str.lower() == anime_name.lower()]
        if anime_row.empty:
            print(f"El anime '{anime_name}' no se pudo encontrar.")
            return None

        anime_id = anime_row['anime_id'].values[0]
        if anime_id not in self.corrMatrix.columns:
            print(f"No se pudo recomendar el anime '{anime_name}' por manca de ratings.")
            return None

        sims = self.corrMatrix[anime_id].dropna()
        sims = sims.map(lambda x: x * rating_value)
        simCandidates = sims.groupby(sims.index).sum()
        simCandidates = simCandidates.drop(anime_id, errors='ignore')
        simCandidates = simCandidates.sort_values(ascending=False)

        simdf = simCandidates.reset_index()
        simdf.columns = ['anime_id', 'score']
        recomendaciones = pd.merge(simdf, self.animes, on='anime_id', how='left')
        recomendaciones.sort_values('score', ascending=False, inplace=True)

        return recomendaciones.head(10)