Esta es una aplicación en Python que sugiere los mejores animes basados en las calificaciones de los usuarios. Los usuarios pueden ingresar un anime que les guste y su calificación, y la aplicación proporcionará una lista de recomendaciones.

---

## FUNCIONALIDADES

- Cargar datos de anime y calificaciones de usuarios desde archivos CSV.
- Calcular puntuaciones de similitud entre animes según las calificaciones.
- Recomendar los 10 mejores animes similares al ingresado por el usuario.
- Interfaz interactiva de línea de comandos.

---

## RQUISITOS

- Python 3.8+
- pandas

Instalar paquetes necesarios con pip:

pip install pandas

---

## ESTRUCTURA DE ARCHIVOS

.
├── main.py                 # Programa principal con interacción del usuario
├── reccs.py                # Clase AnimeRecomendacion (lógica de recomendaciones)
├── rating_limpiado.csv     # Archivo CSV de calificaciones de usuarios
├── anime.csv               # Archivo CSV de información de anime
└── README.md               # Este archivo

---

## USO

1. Asegúrate de que los archivos CSV (`rating_limpiado.csv` y `anime.csv`) estén en el directorio del proyecto.
2. Ejecuta la aplicación:

python main.py

3. Sigue las instrucciones:

- Ingresa tu **ID de usuario** (o escribe `quit` para salir).
- Ingresa el **nombre de un anime** que te guste.
    - En caso de no saber el nombre, puedes escribir una parte y el buscador te puede dar un listado       de animes que coinciden. Encontrando así el anime que buscas. 
- Ingresa una **calificación** para ese anime (1–10).
- Visualiza las **10 principales recomendaciones**.

---

## EJEMPLO

--- RECOMENDACIONES ---
Inserte tu ID de usuario (o escriba 'quit' para salir): 123
Escriba el nombre del anime: Naruto
Escriba el rating del anime (1–10): 8

Top 10 recomendaciones
========================================
Bleach (score: 64.25)
One Piece (score: 60.10)
Dragon Ball Z (score: 58.75)
...

---

## NOTAS

- Los nombres de los animes no distinguen entre mayúsculas y minúsculas.
- Las calificaciones deben ser números del 1 al 10.
- Si un anime no se encuentra en la base de datos, la aplicación solicitará otro.

---

## LICENCIA

Este proyecto es de código abierto y libre para usar.
