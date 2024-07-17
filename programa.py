from base_datos import insertar_contacto, modificar_contacto, eliminar_contacto, listar_contactos
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from clases import Contacto
import os
import sys

class Menu:
    def validar_entero(self):
        while True:
            try:
                n = int(input("[>] "))
                break
            except ValueError:
                print("[!] DEBES INGRESAR UN VALOR ENTERO A.")
        return n
    
    def comprobar_texto(self):
        txt = input("[>] ").strip().upper()
        while len(txt) == 0:
            print("[!] DEBES INGRESAR POR LO MENOS UN CARACTER. VUELTA A INTENTARLO.")
            txt = input("[>] ").strip().upper()
        return txt

    def volver_menu(self):
        print("[!] INGRESE CUALQUIER VALOR PARA VOLVER AL MENU.")
        input("[>] ")

    def limpiar(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def inicializar_mongodb(self):
        direccion = "mongodb://localhost:27017/"
        nombre_bd = "agenda"
        nombre_coleccion = "contactos"

        print("[!] Buscando servicios de MongoDB en 'localhost:27017'...")
        try:
            cliente = MongoClient(direccion, serverSelectionTimeoutMS=1000)
            cliente.admin.command('ping')
            listado_bd= cliente.list_database_names()
            
            print("[!] Instancia de MongoDB encontrada, conectando...")

            if nombre_bd in listado_bd:
                print(f"[!] Conectándose a base de datos '{nombre_bd}'...")
                basededatos = cliente[nombre_bd]
                if nombre_coleccion in basededatos.list_collection_names():
                    print(f"[!] Conectándose a colección '{nombre_coleccion}'.")
                else:
                    print(f"[!] La colección '{nombre_coleccion}' no está registrada. Creando colección.")
                    
                    basededatos = cliente[nombre_bd]
                    coleccion = basededatos[nombre_coleccion]
                    coleccion.insert_one({"temp": "data"})
                    coleccion.delete_one({"temp": "data"})

            else:
                print(f"[!] La base de datos '{nombre_bd}' no está registrada. Creando base de datos y colección 'contactos'...")

                basededatos = cliente[nombre_bd]
                coleccion = basededatos[nombre_coleccion]
                coleccion.insert_one({"temp": "data"})
                coleccion.delete_one({"temp": "data"})
            
        except ConnectionFailure:
            print("[!] No es posible entablar conexión con instancia de MongoDB en 'localhost:27017'.")
            print("[!] Asegúrate de que el servicio de MongoDB esté incializado y vuelve a ejecutar el programa.")
            print(" ")
            input("[>] Ingrese cualquier valor para cerrar el programa: ")
            sys.exit()


    def imprimir_menu(self):
        print("""BIENVENIDO. INGRESE UN ENTERO ACORDE A LA ACCION QUE DESEA REALIZAR:
        
    [1] Ingresar nuevo contacto.
    """)
        
    def ingresar_contacto(self):
        
        nombre = self.comprobar_texto()
        edad = int(input("Ingrese la edad: "))
        categoria = input("Ingrese la categoría de contacto (particular, comercial, trabajo): ")
        direccion = input("Ingrese la dirección: ")
        telefono = int(input("Ingrese el teléfono: "))
        es_favorito = input("¿Es favorito? (s/n): ").lower() == 's'
        detalles_contacto = [{'categoria': categoria, 'direccion': direccion, 'telefono': telefono}]
        contacto = Contacto(nombre, edad, detalles_contacto,)
        insertar_contacto(contacto)
        print("Contacto agregado.")

    def abrir_interfaz(self):
        while True:
            self.imprimir_menu()
            opcion = self.validar_entero()
            
            if opcion == 1:
                self.ingresar_contacto()

            elif opcion == 2:
                nombre = input("Ingrese el nombre del contacto a modificar: ")
                nuevos_datos = {'edad': int(input("Ingrese la nueva edad: "))}
                modificar_contacto(nombre, nuevos_datos)
                print("Contacto modificado.")

            elif opcion == 3:
                nombre = input("Ingrese el nombre del contacto a eliminar: ")
                eliminar_contacto(nombre)
                print("Contacto eliminado.")

            elif opcion == 4:
                contactos = listar_contactos()
                for contacto in contactos:
                    print(contacto)

            elif opcion == 5:
                print("[!] FINALIZANDO PROGRAMA.")
                break

            else:
                print("(!) VALOR NO ASIGNADO A UNA OPCION.")
                self.volver_menu()

    def ejecutar_programa(self):
        self.limpiar()
        self.inicializar_mongodb()
        print("")
        self.abrir_interfaz()

Menu().ejecutar_programa()