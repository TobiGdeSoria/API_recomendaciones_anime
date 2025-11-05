from reccs import AnimeRecomendacion
import sys
import pandas as pd
import json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

DIRECTORIO_RATINGS = r".\rating_limpiado.csv"
DIRECTORIO_ANIME = r".\anime.csv"

console = Console()


def main():
    console.print("[bold khaki1]Cargando y entrenando el sistema de recomendaciones.[/bold khaki1]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        progress.add_task(description="Entrenando el algoritmo (esto puede tardar un rato)...", total=None)
        recomendacion = AnimeRecomendacion(DIRECTORIO_RATINGS, DIRECTORIO_ANIME)
    console.print("[bold green]Entrenamiento completado.[/bold green]")

    ratings_df = pd.read_csv(DIRECTORIO_RATINGS)

    while True:
        console.print("\n[bold aquamarine1]--- SISTEMA DE RECOMENDACIONES DE ANIME ---[/bold aquamarine1]")
        user_input = input("Inserte tu ID de usuario (o escribe 'exit' para salir): ").strip()

        if user_input.lower() == 'exit':
            console.print("[bold green]Hasta pronto! :][/bold green]")
            sys.exit()

        if not user_input.isdigit():
            console.print("[bold red]Por favor, ingresa un número válido o 'exit' para salir.[/bold red]")
            continue

        user_id = int(user_input)
        console.print(f"ID de usuario ingresado: [bold khaki1]{user_id}[/bold khaki1]")

        while True:
            console.print("\n[bold steel_blue1]--- MENÚ ---[/bold steel_blue1]")
            console.print("1.- Obtener recomendaciones")
            console.print("2.- Ver animes calificados")
            console.print("3.- Cambiar de usuario")
            console.print("4.- Agregar/Actualizar calificación de un anime")
            console.print("5.- Salir")

            opcion = input("Seleccione una opción (1–5): ").strip()

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
                            console.print("\n[bold khaki1]No se encontró un anime con ese nombre exacto, pero encontramos coincidencias:[/bold khaki1]")
                            for name in matches['name']:
                                console.print(f"- {name}")
                            console.print("\nPor favor, intenta escribir el nombre nuevamente.")
                            continue
                        else:
                            console.print(f"\n[bold red]El anime '{nombre_anime}' no se encuentra en la base de datos.[/bold red]")
                            continue
                    break

                try:
                    rating_value = float(input("Escriba el rating del anime (1–10): ").strip())
                    if not (1 <= rating_value <= 10):
                        raise ValueError
                except ValueError:
                    console.print("[bold red]Input inválido. Por favor inserte un número del 1 al 10.[/bold red]")
                    continue

                recomendaciones = recomendacion.get_recommendations(nombre_anime, rating_value)

                if recomendaciones is None or recomendaciones.empty:
                    console.print(f"[bold red]El anime '{nombre_anime}' no se pudo recomendar por falta de datos o no existe.[/bold red]")
                else:
                    console.print("\n[bold aquamarine1]Top 10 recomendaciones:[/bold aquamarine1]")
                    console.print("=" * 40)
                    for _, row in recomendaciones.iterrows():
                        console.print(f"{row['name']} (score: {row['score']:.2f})")

            elif opcion == "2":
                user_ratings = ratings_df[ratings_df['user_id'] == user_id]

                if user_ratings.empty:
                    console.print(f"\n[bold khaki1]El usuario {user_id} no tiene animes calificados aún.[/bold khaki1]")
                else:
                    console.print(f"\n[bold aquamarine1]Animes calificados por el usuario {user_id}:[/bold aquamarine1]")
                    console.print("=" * 40)
                    merged = user_ratings.merge(
                        recomendacion.animes[['anime_id', 'name']],
                        on='anime_id',
                        how='left'
                    )
                    for _, row in merged.iterrows():
                        console.print(f"{row['name']} — Calificación: [bold khaki1]{row['rating']}[/bold khaki1]")

            elif opcion == "3":
                break

            elif opcion == "4":
                while True:
                    nombre_anime = input("Escriba el nombre del anime a calificar: ").strip()
                    
                    lower_input = nombre_anime.lower()
                    matches = recomendacion.animes[
                        recomendacion.animes['name'].str.lower().str.contains(lower_input, na=False)
                    ]

                    if nombre_anime.lower() not in recomendacion.animes['name'].str.lower().values:
                        if not matches.empty:
                            console.print("\n[bold khaki1]No se encontró un anime con ese nombre exacto, pero encontramos coincidencias:[/bold khaki1]")
                            for name in matches['name']:
                                console.print(f"- {name}")
                            console.print("\nPor favor, intenta escribir el nombre nuevamente.")
                            continue
                        else:
                            console.print(f"\n[bold red]El anime '{nombre_anime}' no se encuentra en la base de datos.[/bold red]")
                            continue
                    break

                try:
                    rating_value = float(input("Escriba la calificación (1–10): ").strip())
                    if not (1 <= rating_value <= 10):
                        raise ValueError
                except ValueError:
                    console.print("[bold red]Input inválido. Por favor inserte un número del 1 al 10.[/bold red]")
                    continue

                anime_row = recomendacion.animes[recomendacion.animes['name'].str.lower() == nombre_anime.lower()]
                anime_id = anime_row['anime_id'].values[0]

                existing_index = ratings_df[
                    (ratings_df['user_id'] == user_id) & (ratings_df['anime_id'] == anime_id)
                ].index

                if not existing_index.empty:
                    ratings_df.loc[existing_index[0], 'rating'] = rating_value
                    console.print(f"[bold yellow]Calificación actualizada para '{nombre_anime}'[/bold yellow]")
                else:
                    new_row = pd.DataFrame({'user_id': [user_id], 'anime_id': [anime_id], 'rating': [rating_value]})
                    ratings_df = pd.concat([ratings_df, new_row], ignore_index=True)
                    console.print(f"[bold green]Calificación agregada correctamente para '{nombre_anime}'[/bold green]")

                ratings_df.to_csv(DIRECTORIO_RATINGS, index=False, encoding="ISO-8859-1")

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                    console=console
                ) as progress:
                    progress.add_task(description="Actualizando matriz de correlación. Esto tardará un rato...", total=None)
                    recomendacion.update_correlation(ratings_df)

                console.print("[bold green]Matriz de correlación actualizada.[/bold green]")
            
            elif opcion == "5":
                console.print("[bold green]Hasta pronto! :][/bold green]")
                sys.exit()

            else:
                console.print("[bold red]Opción inválida. Por favor elige entre 1 y 5.[/bold red]")


if __name__ == "__main__":
    main()
