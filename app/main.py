import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

RUTA_JSON = "data/clientes.json"

class ClienteModelo(BaseModel):
    nombre: str
    email: str
    telefono: str

def cargar_clientes():
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
 
def guardar_clientes(clientes):
    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)

@app.get("/")
def inicio():
    return {
        "mensaje": "Generacion de la API"
    }


@app.get("/clientes")
def obtener_clientes():
    return cargar_clientes()


@app.get("/clientes/{id_cliente}")
def obtener_cliente(id_cliente: int):
    clientes = cargar_clientes()

    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente

    return {
        "error": "Cliente no encontrado"
    }

@app.post("/clientes", status_code=201)
def agregar_cliente(cliente: ClienteModelo):
    clientes = cargar_clientes()

    nuevo_cliente = {
        "id": len(clientes) + 1,
        "nombre": cliente.nombre,
        "email": cliente.email,
        "telefono": cliente.telefono
    }

    clientes.append(nuevo_cliente)

    guardar_clientes(clientes)

    return {
        "mensaje": "Cliente agregado exitosamente"
    }

@app.put("/clientes/{id_cliente}")
def actualizar_cliente(id_cliente: int, cliente_actualizado: ClienteModelo):
    clientes = cargar_clientes()

    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            datos_modificados = {
                "id": id_cliente,
                "nombre": cliente_actualizado.nombre,
                "email": cliente_actualizado.email,
                "telefono": cliente_actualizado.telefono
            }
            clientes[i] = datos_modificados
            guardar_clientes(clientes)
            return {
                "mensaje": "Cliente actualizado exitosamente"
            }

    return {
        "error": "Cliente no encontrado"
    }

@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    clientes = cargar_clientes()

    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            cliente_eliminado = clientes.pop(i)
            guardar_clientes(clientes)
            return {
                "mensaje": "Cliente eliminado exitosamente"
            }

    return {
        "error": "Cliente no encontrado"
    }