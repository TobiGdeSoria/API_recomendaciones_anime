from flask import Flask, send_from_directory, request
import pandas as pd
import os

app = Flask(__name__)

# === RUTAS ===
base = os.path.dirname(os.path.abspath(__file__))        # carpeta API_recomendaciones_anime
parent = os.path.abspath(os.path.join(base, '..'))       # carpeta Anime

# === CARGA DE DATOS ===
try:
    r_cols = ['user_id', 'anime_id', 'rating']
    ratings = pd.read_csv(os.path.join(base, 'rating_limpiado.csv'),
                          usecols=[0, 1, 2], encoding="ISO-8859-1")
    ratings.columns = r_cols

    a_cols = ['anime_id', 'name']
    animes = pd.read_csv(os.path.join(parent, 'anime copy.csv'),
                         usecols=[0, 1], encoding="ISO-8859-1")
    animes.columns = a_cols

    # === MATRIZ DE CORRELACIÓN ===
    userRatings = ratings.pivot_table(index=['user_id'], columns=['anime_id'], values='rating')
    corrMatrix = userRatings.corr(method='pearson', min_periods=30)

except Exception as e:
    print("⚠️ Error al cargar los CSVs:", e)
    corrMatrix = None
    animes = pd.DataFrame(columns=['anime_id', 'name'])

# === RUTA PRINCIPAL (LOGIN) ===
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            anime_id = int(request.form['anime_id'])
            rating = float(request.form['rating'])

            myRatings = pd.Series({anime_id: rating})
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
            simdf.columns = ['anime_id', 'score']
            recomendaciones = pd.merge(simdf, animes, on='anime_id', how='left')
            recomendaciones = recomendaciones[['name', 'score']].head(10)
            print("\n✅ Recomendaciones generadas:\n", recomendaciones)
        except Exception as e:
            print("⚠️ Error generando recomendaciones:", e)

    # Mostrar el index.html del directorio padre
    return send_from_directory(parent, 'index.html')

# === DASHBOARD ===
@app.route('/dashboard')
def dashboard():
    return send_from_directory(parent, 'dashboard.html')

# === ARCHIVOS ESTÁTICOS ===
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(parent, filename)

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📂 Directorio base:", base)
    print("📁 Directorio superior:", parent)
    print("✅ Intentando arrancar Flask en http://127.0.0.1:5000 ...")
    try:
        app.run(debug=True, host="127.0.0.1", port=5000)
    except Exception as e:
        print("❌ ERROR al arrancar Flask:", e)
