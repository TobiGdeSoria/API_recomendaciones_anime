from reccs import AnimeRecomendacion
import sys
import pandas as pd

DIRECTORIO_RATINGS = r".\rating_limpiado.csv"
DIRECTORIO_ANIME = r".\anime.csv"


def main():
    recomendacion = AnimeRecomendacion(DIRECTORIO_RATINGS, DIRECTORIO_ANIME)
    ratings_df = pd.read_csv(DIRECTORIO_RATINGS)

    while True:
        print("\n--- SISTEMA DE RECOMENDACIONES DE ANIME ---")
        user_input = input("Inserte tu ID de usuario (o escribe 'exit' para salir): ").strip()

        if user_input.lower() == 'exit':
            print("Hasta pronto :]")
            sys.exit()

        if not user_input.isdigit():
            print("Por favor, ingresa un número válido o 'exit' para salir.")
            continue

        user_id = int(user_input)
        print(f"ID de usuario ingresado: {user_id}")

        while True:
            print("\n--- MENÚ ---")
            print("1.- Obtener recomendaciones")
            print("2.- Ver animes calificados")
            print("3.- Cambiar de usuario")
            print("4.- Salir")

            opcion = input("Seleccione una opción (1–4): ").strip()

            if opcion == "1":
                while True:
                    nombre_anime = input("Escriba el nombre del anime: ").strip()
                    if nombre_anime.lower() == 'quit':
                        break

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
                    rating_value = float(input("Escriba el rating del anime (1–10): ").strip())
                    if not (1 <= rating_value <= 10):
                        raise ValueError
                except ValueError:
                    print("Input inválido. Por favor inserte un número del 1 al 10.")
                    continue

                recomendaciones = recomendacion.get_recommendations(nombre_anime, rating_value)
                if recomendaciones is not None and not recomendaciones.empty:
                    print("\nTop 10 recomendaciones")
                    print("=" * 40)
                    for _, row in recomendaciones.iterrows():
                        print(f"{row['name']} (score: {row['score']:.2f})")

            elif opcion == "2":
                user_ratings = ratings_df[ratings_df['user_id'] == user_id]

                if user_ratings.empty:
                    print(f"\nEl usuario {user_id} no tiene animes calificados aún.")
                else:
                    print(f"\nAnimes calificados por el usuario {user_id}:")
                    print("=" * 40)
                    merged = user_ratings.merge(
                        recomendacion.animes[['anime_id', 'name']],
                        on='anime_id',
                        how='left'
                    )
                    for _, row in merged.iterrows():
                        print(f"{row['name']} — Calificación: {row['rating']}")

            elif opcion == "3":
                break

            elif opcion == "4":
                print("Hasta pronto :]")
                sys.exit()

            else:
                print("Opción inválida. Por favor elige entre 1 y 4.")


if __name__ == "__main__":
    main()
