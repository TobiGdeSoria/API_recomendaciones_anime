from reccs import AnimeRecomendacion
import sys

DIRECTORIO_RATINGS = r".\rating_limpiado.csv"
DIRECTORIO_ANIME = r".\anime.csv"

def main():
    recomendacion = AnimeRecomendacion(DIRECTORIO_RATINGS, DIRECTORIO_ANIME)

    while True:
        print("\n--- RECOMENDACIONES ---")
    
        user_input = input("Inserte tu ID de usuario (o escribe 'quit' para salir): ").strip()
    
        if user_input.lower() == 'exit':
            print("Hasta pronto :]")
            sys.exit()
    
        if user_input.isdigit():
            user_id = int(user_input)
            print(f"ID de usuario ingresado: {user_id}")
        else:
            print("Por favor, ingresa un número válido o 'exit' para salir.")
            continue

        while True:
            nombre_anime = input("Escriba el nombre del anime: ").strip()
            if nombre_anime.lower() == 'quit':
                print("Hasta pronto :]")
                sys.exit()
            
            lower_input = nombre_anime.lower()
            
            matches = recomendacion.animes[
                recomendacion.animes['name'].str.lower().str.contains(lower_input, na=False)
            ]

            if nombre_anime.lower() not in recomendacion.animes['name'].str.lower().values:
                if not matches.empty:
                    print("\nNo se encontró un anime con ese nombre exacto, pero encontramos coincidencias:")
                    for name in matches['name']:
                        print(f"- {name}")
                    print("\nPor favor, intenta escribir el nombre nuevamente.")
                    continue
                else:
                    print(f"\nEl anime '{nombre_anime}' no se encuentra en la base de datos.")
                    continue
            break
    
        try:
            rating_value = float(input("Excriba el rating del anime (1–10): ").strip())
            if not (1 <= rating_value <= 10):
                raise ValueError
        except ValueError:
            print("Input invalido. Porfavor inserte un numero del 1 al 10.")
            continue

        recomendaciones = recomendacion.get_recommendations(nombre_anime, rating_value)
        if recomendaciones is not None and not recomendaciones.empty:
            print("\nTop 10 recomendaciones")
            print("=" * 40)
            for _, row in recomendaciones.iterrows():
                print(f"{row['name']} (score: {row['score']:.2f})")

if __name__ == "__main__":
    main()
