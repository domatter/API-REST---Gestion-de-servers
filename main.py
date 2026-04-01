Python 3.10.1 (tags/v3.10.1:2cd268a, Dec  6 2021, 19:10:37) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

FILE = "servers.json"



class Server(BaseModel):
    id: int
    name: str
    ip: str
    ram: str
    size: str


class ServerUpdate(BaseModel):
    name: str
    ip: str
    ram: str
    size: str


# Lire fichier JSON
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


# Write fichier JSON
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# GET Lister serveurs
@app.get("/servers")
def get_servers():
    return load_data()


# POST Créer nouveau server
@app.post("/servers")
def add_server(server: Server):
    data = load_data()

    for s in data:
        if s["id"] == server.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    data.append(server.dict())
    save_data(data)

    return {"message": "Server added", "server": server}


# PUT Modifier serveur
@app.put("/servers/{server_id}")
def update_server(server_id: int, updated_server: ServerUpdate):
    data = load_data()

    for i in range(len(data)):
        if data[i]["id"] == server_id:
            data[i] = {
                "id": server_id,
                "name": updated_server.name,
                "ip": updated_server.ip,
                "ram": updated_server.ram,
                "size": updated_server.size
            }
            save_data(data)
            return {"message": "Server updated", "server": data[i]}

    raise HTTPException(status_code=404, detail="Server not found")


# DELETE Supprimer serveur
@app.delete("/servers/{server_id}")
def delete_server(server_id: int):
    data = load_data()

    for s in data:
        if s["id"] == server_id:
            data.remove(s)
            save_data(data)
            return {"message": "Server deleted", "id": server_id}

    raise HTTPException(status_code=404, detail="Server not found")