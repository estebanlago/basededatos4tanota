from base_datos import insertar_contacto, modificar_contacto, eliminar_contacto, listar_contactos, coleccion_contactos
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from clases import Contacto
import os
import sys

class Menu:
    def validar_entero(self, mensaje="[>] "):
        while True:
            try:
                n = int(input(mensaje))
                break
            except ValueError:
                print("[!] DEBES INGRESAR UN VALOR ENTERO.")
        return n
    
    def comprobar_texto(self, mensaje):
        txt = input(mensaje).strip()
        while len(txt) == 0:
            print("[!] DEBES INGRESAR POR LO MENOS UN CARACTER. VUELTA A INTENTARLO.")
            txt = input(mensaje).strip()
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
            print("[!] Asegúrate de que el servicio de MongoDB esté inicializado y vuelve a ejecutar el programa.")
            print(" ")
            input("[>] Ingrese cualquier valor para cerrar el programa: ")
            sys.exit()


    def imprimir_menu(self):
        print("""BIENVENIDO. INGRESE UN ENTERO ACORDE A LA ACCION QUE DESEA REALIZAR:
        
    [1] Ingresar nuevo contacto.
    [2] Modificar contacto.
    [3] Eliminar contacto.
    [4] Listar contactos.
    [5] SALIR.
    """)
        
    def ingresar_contacto(self): 
        nombre = self.comprobar_texto("Ingrese el nombre: ")
        edad = self.validar_entero("Ingrese la edad: ")
        while True:
            categoria = self.comprobar_texto("Ingrese la categoría de contacto (particular, comercial, trabajo): ")
            if categoria.lower() not in ["particular", "comercial", "trabajo"]:
                print("[!] DEBE INGRESAR UNA CATEGORIA. VUELTA A INTENTARLO.")
                continue
            direccion = self.comprobar_texto("Ingrese la dirección: ")
            telefono = self.validar_entero("Ingrese el teléfono: ")
            break
        favorito = input("¿Es favorito? (s/n): ").strip().lower() == 's'
        detalles_contacto = [{'categoria': categoria, 'direccion': direccion, 'telefono': telefono}]
        contacto = Contacto(nombre, edad, detalles_contacto, favorito)
        
        insertar_contacto(contacto)
        print("Contacto agregado.")

    def modificar_contacto(self):
        nombre = self.comprobar_texto("Ingrese el nombre del contacto a modificar: ")
        contacto = coleccion_contactos.find_one({"nombre": nombre})
        detalles_contacto = contacto.get("detalles_contacto", [])
        
        if not contacto:
            print("El contacto no se encuentra en la base de datos.")
            return
        
        while True:
            categoria = self.comprobar_texto("Ingrese la categoría de contacto (particular, comercial, trabajo): ")
            if categoria.lower() not in ["particular", "comercial", "trabajo"]:
                print("[!] DEBE INGRESAR UNA CATEGORIA. VUELTA A INTENTARLO.")
                continue
            direccion = self.comprobar_texto("Ingrese la nueva dirección: ")
            telefono = self.validar_entero("Ingrese el nuevo teléfono: ")
            break
        
        detalles_contacto.append({
            "categoria": categoria,
            "direccion": direccion,
            "telefono": telefono
        }) 
        

        modificar_contacto(nombre, detalles_contacto)
        print("Contacto modificado.")

    def abrir_interfaz(self):
        while True:
            self.imprimir_menu()
            opcion = self.validar_entero()
            
            if opcion == 1:
                self.ingresar_contacto()

            elif opcion == 2:
                self.modificar_contacto()

            elif opcion == 3:
                nombre = input("Ingrese el nombre del contacto a eliminar: ")
                eliminar_contacto(nombre)
                print("Contacto eliminado.")

            elif opcion == 4:
                listar_contactos()

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