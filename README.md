# Cloud-Computing-Tarea1

**Autor:** Javier Alejandro Castro Barreto

API REST desarrollada con Flask y SQLite para gestionar usuarios, productos y órdenes dentro del contexto de un Ecomerce.

## Tecnologías

- Flask
- SQLite
- Docker
- Postman

## Ejecución

1. Instalar dependencias:

```bash
pip install flask
```

2. Iniciar la aplicación:

```bash
python app.py
```

## Endpoints

- `GET /users`
- `POST /users`
- `GET /products`
- `POST /products`
- `POST /orders`
- `GET /orders`
- `GET /orders/<id>`

## Tablas

- `users`: almacena la información básica de los usuarios, como nombre y correo.
- `products`: guarda los productos registrados, junto con su precio y stock disponible.
- `orders`: registra cada orden realizada por un usuario y el total de la compra.
- `order_items`: relaciona cada orden con los productos incluidos y la cantidad solicitada.

## Colección de Postman

El archivo `api-ecomerce.postman_collection.json` contiene requests para probar la API.

Cambiar la IP de las URLs en Postman por la IP pública de tu instancia.

```text
http://IP_PUBLICA:8000/
```
