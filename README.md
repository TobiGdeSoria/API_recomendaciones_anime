Esta es una aplicación en Python que sugiere los mejores animes basados en las calificaciones de los usuarios. Los usuarios entran en su usuario, y se les dará la opción de ver que animes ha calificado, o ingresar un anime que les guste y su calificación, la aplicación automaticamente proporcionará una lista de recomendaciones.

---

## FUNCIONALIDADES

- Cargar datos de anime y calificaciones de usuarios desde archivos CSV o JSON.
- Calcular puntuaciones de similitud entre animes según las calificaciones.
- Recomendar los 10 mejores animes similares al ingresado por el usuario.
- Interfaz interactiva y creativa de línea de comandos.

---

## RQUISITOS

- Python 3.8+
- pandas
- rich

Instalar paquetes necesarios con pip:

pip install pandas
pip install rich

---

## ESTRUCTURA DE ARCHIVOS

.
├── main.py                 # Programa principal con interacción del usuario
├── corr_matrix.pkl         # Matriz de correlación para que el programa solo entrene el algoritmo la primera vez (hace la app mas rápida) **--> aparece una vez ejecutada la aplicación por primera vez**
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
- Elije entre las opciones del menú:
        - Obtener recomendaciones.
                - Ingresa el **nombre de un anime** que te guste.
                    - En caso de no saber el nombre, puedes escribir una parte y el buscador te puede dar un listado de animes que coinciden. Encontrando así el anime que buscas. 
                - Ingresa una **calificación** para ese anime (1–10).
                - Visualiza las **15 principales recomendaciones**.
        - Ver tus animes calificados.
        - Cambiar de usuario.

---

## EJEMPLO PEDIR RECOMENDACIONES


--- SISTEMA DE RECOMENDACIONES DE ANIME ---
Inserte tu ID de usuario (o escriba 'quit' para salir): 23

--- MENÚ ---
Seleccione una opción (1–4): 1 (Obtener recomendaciones)
Escriba el nombre del anime: bleach
Escriba el rating del anime (1–10): 8

Top 10 recomendaciones
========================================
Naruto (score: 4.42)
Fairy Tail (score: 4.30)
Dragon Ball GT (score: 4.08)
...

---

## NOTAS

- Los nombres de los animes no distinguen entre mayúsculas y minúsculas.
- Las calificaciones deben ser números del 1 al 10.
- Si un anime no se encuentra en la base de datos, la aplicación solicitará otro.

---

## LICENCIA

Este proyecto es de código abierto y libre para usar.
