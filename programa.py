from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import sys

direccion = "mongodb://localhost:27017/"
nombre_bd = "agenda"
nombre_coleccion = "contactos"


def limpiar():
    os.system('cls' if os.name=='nt' else 'clear')

def inicializar_mongodb():
    print("[!] Buscando servicios de MongoDB en 'localhost:27017'...")
    try:
        client = MongoClient(direccion, serverSelectionTimeoutMS=1000)
        client.admin.command('ping')
        listado_bd= client.list_database_names()
        
        print("[!] Instancia de MongoDB encontrada, conectando...")

        if nombre_bd in listado_bd:
            print(f"[!] Conectándose a base de datos '{nombre_bd}'...")
            basededatos = client[nombre_bd]
            if nombre_coleccion in basededatos.list_collection_names():
                print(f"[!] Conectándose a colección '{nombre_coleccion}'.")
            else:
                print(f"[!] La colección '{nombre_coleccion}' no está registrada. Creando colección.")
                
                basededatos = client[nombre_bd]
                coleccion = basededatos[nombre_coleccion]
                coleccion.insert_one({"temp": "data"})
                coleccion.delete_one({"temp": "data"})

        else:
            print(f"[!] La base de datos '{nombre_bd}' no está registrada. Creando base de datos y colección 'contactos'...")

            basededatos = client[nombre_bd]
            coleccion = basededatos[nombre_coleccion]
            coleccion.insert_one({"temp": "data"})
            coleccion.delete_one({"temp": "data"})
        
    except ConnectionFailure:
        print("[!] No es posible entablar conexión con instancia de MongoDB en 'localhost:27017'.")
        print("[!] Asegúrate de que el servicio de MongoDB esté incializado y vuelve a ejecutar el programa.")
        print(" ")
        input("[>] Ingrese cualquier valor para cerrar el programa: ")
        sys.exit()

limpiar()
inicializar_mongodb()


