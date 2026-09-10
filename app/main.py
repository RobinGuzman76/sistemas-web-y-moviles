import json

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {
        "mensaje": "Generacion de la API"
    }


@app.get("/clientes")
def obtener_clientes():
    with open("data/clientes.json", "r") as archivo:
        clientes = json.load(archivo)
    return clientes


@app.get("/clientes/{id_cliente}")
def obtener_cliente(id_cliente: int):
    with open("data/clientes.json", "r") as archivo:
        clientes = json.load(archivo)

    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente

    return {
        "error": "Cliente no encontrado"
    }