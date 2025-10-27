from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load datasets
r_cols = ['user_id', 'anime_id', 'rating']
ratings = pd.read_csv('C:\\Users\\tyfae\\Downloads\\datos\\rating_limpiado.csv', sep=',', names=r_cols, usecols=range(3), encoding="ISO-8859-1", skiprows=1, low_memory=False)

a_cols = ['anime_id', 'name']
animes = pd.read_csv('C:\\Users\\tyfae\\Downloads\\datos\\anime.csv', sep=',', names=a_cols, usecols=range(2), encoding="ISO-8859-1", skiprows=1)

# Precompute user-anime matrix
userRatings = ratings.pivot_table(index=['user_id'], columns=['anime_id'], values='rating')
corrMatrix = userRatings.corr(method='pearson', min_periods=30)

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    if request.method == 'POST':
        # Get user input
        anime_id = int(request.form['anime_id'])
        rating = float(request.form['rating'])
        
        # Create a user rating series
        myRatings = pd.Series({anime_id: rating})
        
        # Generate recommendations
        simCandidates = pd.Series(dtype=float)
        for anime, rating_val in myRatings.items():
            if anime not in corrMatrix.columns:
                continue
            sims = corrMatrix[anime].dropna()
            sims = sims.map(lambda x: x * rating_val)
            simCandidates = pd.concat([simCandidates, sims])
        simCandidates = simCandidates.groupby(simCandidates.index).sum()
        simCandidates = simCandidates.drop(myRatings.index, errors='ignore')
        simCandidates = simCandidates.sort_values(ascending=False)
        
        simdf = simCandidates.reset_index()
        simdf.columns = ['anime_id','score']
        recomendaciones = pd.merge(simdf, animes, on='anime_id', how='left')
        recomendaciones = recomendaciones[['name', 'score']].head(10)
        
    return render_template('index.html', recommendations=recomendaciones)

if __name__ == '__main__':
    app.run(debug=True)
