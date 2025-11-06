import sys
import time
import pandas as pd
import requests
import threading
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

DIRECTORIO_RATINGS = r".\rating_limpiado.csv"
ANIME_CSV = r".\anime.csv"
API_URL = "http://127.0.0.1:8000"

console = Console()
CACHE_FILE = "corr_matrix.pkl"

def update_correlation_async(force=False):
    """Call the API to update correlation in the background."""
    try:
        requests.post(f"{API_URL}/update", params={"force": str(force).lower()})
    except Exception as e:
        console.print(f"[bold red]Error actualizando la matriz de correlación: {e}[/bold red]")

def main():
    if not os.path.exists(CACHE_FILE):
        console.print("[bold khaki1]Generando la matriz de correlación. Esto puede tardar un momento...[/bold khaki1]")
        thread = threading.Thread(target=update_correlation_async, args=(False,), daemon=True)
        thread.start()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            task = progress.add_task(description="Generando matriz de correlación...", total=None)
            while thread.is_alive():
                time.sleep(0.1)

        console.print("[bold green]Matriz de correlación generada.[/bold green]\n")
    else:
        console.print("[bold green]Matriz de correlación existente cargada.[/bold green]\n")

    ratings_df = pd.read_csv(DIRECTORIO_RATINGS)
    animes_df = pd.read_csv(ANIME_CSV, usecols=[0, 1], names=['anime_id', 'name'], skiprows=1)

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
                    nombre_anime = input("Escriba el nombre del anime (o 'quit' para salir): ").strip()
                    if nombre_anime.lower() == 'quit':
                        break

                    try:
                        rating_value = float(input("Escriba el rating del anime (1–10): ").strip())
                        if not (1 <= rating_value <= 10):
                            raise ValueError
                    except ValueError:
                        console.print("[bold red]Input inválido. Por favor inserte un número del 1 al 10.[/bold red]")
                        continue

                    response = requests.get(
                        f"{API_URL}/recommendations",
                        params={"anime": nombre_anime, "rating": rating_value}
                    )

                    if response.status_code != 200:
                        console.print(f"[bold red]Error al obtener recomendaciones: {response.text}[/bold red]")
                        continue

                    recomendaciones = response.json()
                    if "error" in recomendaciones:
                        lower_input = nombre_anime.lower()
                        matches = animes_df[animes_df['name'].str.lower().str.contains(lower_input, na=False)]
                        if not matches.empty:
                            console.print("\n[bold khaki1]No se encontró un anime exacto, pero encontramos coincidencias:[/bold khaki1]")
                            for name in matches['name']:
                                console.print(f"- {name}")
                            console.print("Por favor, intenta escribir el nombre nuevamente.")
                            continue
                        else:
                            console.print(f"[bold red]{recomendaciones['error']}[/bold red]")
                            continue

                    console.print("\n[bold aquamarine1]Top 10 recomendaciones:[/bold aquamarine1]")
                    console.print("=" * 40)
                    for rec in recomendaciones:
                        console.print(f"{rec['name']} (score: {rec['score']:.2f})")
                    break

            elif opcion == "2":
                user_ratings = ratings_df[ratings_df['user_id'] == user_id]
                if user_ratings.empty:
                    console.print(f"\n[bold khaki1]El usuario {user_id} no tiene animes calificados aún.[/bold khaki1]")
                else:
                    console.print(f"\n[bold aquamarine1]Animes calificados por el usuario {user_id}:[/bold aquamarine1]")
                    console.print("=" * 40)
                    merged = user_ratings.merge(animes_df, on='anime_id', how='left')
                    for _, row in merged.iterrows():
                        console.print(f"{row['name']} — Calificación: [bold khaki1]{row['rating']}[/bold khaki1]")

            elif opcion == "3":
                break

            elif opcion == "4":
                while True:
                    nombre_anime = input("Escriba el nombre del anime a calificar: ").strip()
                    lower_input = nombre_anime.lower()
                    matches = animes_df[animes_df['name'].str.lower().str.contains(lower_input, na=False)]

                    if nombre_anime.lower() not in animes_df['name'].str.lower().values:
                        if not matches.empty:
                            console.print("\n[bold khaki1]No se encontró un anime exacto, pero encontramos coincidencias:[/bold khaki1]")
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

                anime_row = animes_df[animes_df['name'].str.lower() == nombre_anime.lower()]
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

                thread = threading.Thread(target=update_correlation_async, args=(True,), daemon=True)
                thread.start()

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                    console=console
                ) as progress:
                    task = progress.add_task(description="Actualizando matriz de correlación...", total=None)
                    while thread.is_alive():
                        time.sleep(0.1)

                console.print("[bold green]Matriz de correlación actualizada.[/bold green]")

            elif opcion == "5":
                console.print("[bold green]Hasta pronto! :][/bold green]")
                sys.exit()

            else:
                console.print("[bold red]Opción inválida. Por favor elige entre 1 y 5.[/bold red]")


if __name__ == "__main__":
    main()
