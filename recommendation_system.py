"""Sistema introductorio de recomendacion de productos por similitud."""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def crear_catalogo() -> pd.DataFrame:
    """Crea un catalogo de ejemplo con caracteristicas descriptivas."""
    productos = [
        {
            "nombre": "Laptop para estudiantes",
            "categoria": "electronica",
            "descripcion": "computadora portatil ligera para estudiar y trabajar",
        },
        {
            "nombre": "Laptop para videojuegos",
            "categoria": "electronica",
            "descripcion": "computadora portatil potente para videojuegos y graficos",
        },
        {
            "nombre": "Teclado mecanico",
            "categoria": "electronica",
            "descripcion": "teclado para computadora con teclas mecanicas para jugar",
        },
        {
            "nombre": "Audifonos inalambricos",
            "categoria": "audio",
            "descripcion": "audifonos bluetooth para escuchar musica y viajar",
        },
        {
            "nombre": "Bocina bluetooth",
            "categoria": "audio",
            "descripcion": "bocina portatil inalambrica para escuchar musica",
        },
        {
            "nombre": "Novela de ciencia ficcion",
            "categoria": "libros",
            "descripcion": "libro de ciencia ficcion sobre viajes espaciales",
        },
        {
            "nombre": "Libro de programacion",
            "categoria": "libros",
            "descripcion": "libro educativo para aprender programacion en Python",
        },
        {
            "nombre": "Mochila para laptop",
            "categoria": "accesorios",
            "descripcion": "mochila resistente para llevar computadora y accesorios",
        },
    ]
    return pd.DataFrame(productos)


def entrenar_modelo(productos: pd.DataFrame):
    """Convierte categoria y descripcion en vectores y calcula similitudes."""
    # Se combinan las caracteristicas de texto para representar cada producto.
    caracteristicas = (
        productos["categoria"] + " " + productos["descripcion"]
    )

    # TF-IDF asigna mayor peso a palabras utiles para distinguir productos.
    vectorizador = TfidfVectorizer()
    matriz_productos = vectorizador.fit_transform(caracteristicas)

    # La similitud coseno compara cada producto con todos los demas.
    matriz_similitud = cosine_similarity(matriz_productos)
    return matriz_similitud


def recomendar_productos(
    nombre_producto: str,
    productos: pd.DataFrame,
    matriz_similitud,
    cantidad: int = 3,
) -> pd.DataFrame:
    """Devuelve los productos mas similares al producto ingresado."""
    # La busqueda no distingue mayusculas ni espacios al inicio o al final.
    nombre_buscado = nombre_producto.strip().casefold()
    nombres = productos["nombre"].str.casefold()
    coincidencias = productos.index[nombres == nombre_buscado].tolist()

    if not coincidencias:
        raise ValueError(f"No se encontro el producto: {nombre_producto}")
    if cantidad < 1:
        raise ValueError("La cantidad de recomendaciones debe ser al menos 1.")

    indice_producto = coincidencias[0]
    puntuaciones = matriz_similitud[indice_producto]

    # Se excluye el producto consultado y se ordena por similitud descendente.
    indices_ordenados = puntuaciones.argsort()[::-1]
    indices_recomendados = [
        indice
        for indice in indices_ordenados
        if indice != indice_producto
    ][:cantidad]

    recomendaciones = productos.iloc[indices_recomendados][
        ["nombre", "categoria", "descripcion"]
    ].copy()
    recomendaciones["similitud"] = puntuaciones[indices_recomendados]
    return recomendaciones.reset_index(drop=True)


def main() -> None:
    """Prepara el modelo y permite consultar recomendaciones."""
    # Se crea el catalogo y se ajusta el modelo antes de recibir consultas.
    productos = crear_catalogo()
    matriz_similitud = entrenar_modelo(productos)

    print("Productos disponibles:")
    for nombre in productos["nombre"]:
        print(f"- {nombre}")

    nombre_producto = input("\nEscribe el nombre de un producto: ")

    try:
        recomendaciones = recomendar_productos(
            nombre_producto, productos, matriz_similitud
        )
    except ValueError as error:
        print(error)
        return

    print("\nProductos recomendados:")
    print(recomendaciones.to_string(index=False))


if __name__ == "__main__":
    main()