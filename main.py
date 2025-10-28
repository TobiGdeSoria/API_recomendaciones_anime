from reccs import AnimeRecomendacion
import sys

DIRECTORIO_RATINGS = r".\rating_limpiado.csv"
DIRECTORIO_ANIME = r".\anime.csv"

def main():
    recomendacion = AnimeRecomendacion(DIRECTORIO_RATINGS, DIRECTORIO_ANIME)

    while True:
        print("\n--- RECOMENDACIONES ---")
        user_id = input("Inserte tu ID de usuario (o escribe 'quit' para salir): ").strip()
        if user_id.lower() == 'quit':
            print("Hasta pronto :]")
            sys.exit()

        nombre_anime = input("Escriba el nombre del anime: ").strip()

        if nombre_anime.lower() not in recomendacion.animes['name'].str.lower().values:
            print(f"El anime '{nombre_anime}' no se encuentra en la base de datos.")
            continue

        try:
            rating_value = float(input("Excriba el rating del anime (1–10): ").strip())
            if not (1 <= rating_value <= 10):
                raise ValueError
        except ValueError:
            print("Input invalido. Porfavor inserte un numero del 1 al 10.")
            continue

        recomendaciones = recomendacion.get_recomendaciones(nombre_anime, rating_value)
        if recomendaciones is not None and not recomendaciones.empty:
            print("\nTop 10 recomendaciones")
            print("=" * 40)
            for _, row in recomendaciones.iterrows():
                print(f"{row['name']} (score: {row['score']:.2f})")

if __name__ == "__main__":
    main()
