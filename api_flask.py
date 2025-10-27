from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data
r_cols = ['user_id', 'anime_id', 'rating']
ratings = pd.read_csv(
    'C:\\Users\\tyfae\\Downloads\\datos\\rating_limpiado.csv', 
    sep=',', names=r_cols, usecols=range(3), encoding="ISO-8859-1", skiprows=1, low_memory=False
)

a_cols = ['anime_id', 'name']
animes = pd.read_csv(
    'C:\\Users\\tyfae\\Downloads\\datos\\anime.csv', 
    sep=',', names=a_cols, usecols=range(2), encoding="ISO-8859-1", skiprows=1
)

# Pivot user-anime ratings
userRatings = ratings.pivot_table(index='user_id', columns='anime_id', values='rating')

# Correlation matrix
corrMatrix = userRatings.corr(method='pearson', min_periods=30)

# Create a dictionary to map anime names to IDs
anime_name_to_id = dict(zip(animes['name'], animes['anime_id']))

@app.route("/", methods=['GET', 'POST'])
def index():
    recommendations = []
    anime_names = sorted(animes['name'].tolist())  # Sorted list for dropdown

    if request.method == 'POST':
        anime_name = request.form['anime_name']
        rating = float(request.form['rating'])

        anime_id = anime_name_to_id.get(anime_name)
        if not anime_id:
            return render_template('index.html', recommendations=[], anime_names=anime_names, error="Anime not found")

        myRatings = pd.Series({anime_id: rating})

        simCandidates = pd.Series(dtype=float)
        for anime, rating in myRatings.items():
            if anime not in corrMatrix.columns:
                continue
            sims = corrMatrix[anime].dropna()
            sims = sims.map(lambda x: x * rating)
            simCandidates = pd.concat([simCandidates, sims])

        simCandidates = simCandidates.groupby(simCandidates.index).sum()
        simCandidates = simCandidates.drop(myRatings.index, errors='ignore')
        simCandidates = simCandidates.sort_values(ascending=False)

        simdf = simCandidates.reset_index()
        simdf.columns = ['anime_id','score']
        recomendaciones = pd.merge(simdf, animes, on='anime_id', how='left')
        recomendaciones.sort_values('score', ascending=False, inplace=True)

        recommendations = recomendaciones[['name','score']].head(10).values.tolist()

    return render_template('index.html', recommendations=recommendations, anime_names=anime_names)

if __name__ == "__main__":
    app.run(debug=True)
