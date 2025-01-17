from base_datos import insertar_contacto, modificar_contacto, eliminar_contacto, listar_contactos
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from clases import Contacto
import os
import sys

# Conexión a la base de datos para usar la colección
cliente = MongoClient('mongodb://localhost:27017/')
bd = cliente['agenda']
coleccion_contactos = bd['contactos']

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
    [0] SALIR.
    """)

# Ingresar contacto 
    def ingresar_contacto(self): 
        self.limpiar()
        print("INGRESE EL NOMBRE DEL NUEVO CONTACTO A AGREGAR: ")
        print(" ")
        nombre = self.comprobar_texto("[>] ")
        print(" ")
        print("INGRESE LA EDAD DE CONTACTO: ")
        print(" ")
        edad = self.validar_entero("[>] ")
        # Validación de categoría para que pueda ser ingresada como texto o como número (string)
        while True:
            print(" ")
            print("INGRESE LA CATEGORIA DE CONTACTO ([1] PARTICULAR, [2] COMERCIAL, [3] TRABAJO)")
            print(" ")
            categoria_input = self.comprobar_texto("[>] ")
            if categoria_input == "1":
                categoria = "particular"
            elif categoria_input == "2":
                categoria = "comercial"
            elif categoria_input == "3":
                categoria = "trabajo"
            else:
                categoria = categoria_input.lower()
                
            if categoria.lower() not in ["particular", "comercial", "trabajo"]:
                print("[!] DEBE INGRESAR UNA CATEGORIA. VUELTA A INTENTARLO.")
                print(" ")
                continue
            print(" ")
            print("INGRESE LA DIRECCION: ")
            print(" ")
            direccion = self.comprobar_texto("[>] ")
            print(" ")
            print("INGRESE EL TELEFONO: ")
            print(" ")
            telefono = self.validar_entero("[>] ")
            break
        
        print(" ")
        print("¿ES FAVORITO? (S/N): ")
        print(" ")
        favorito = input("[>] ").strip().lower()
        print(" ")
        while True:
            try:
                if favorito.lower() == "s":
                    favorito = True
                    break
                elif favorito.lower() == "n":
                    favorito = False
                    break
                else:
                    print("[!] DEBE INGRESAR UNA OPCIÓN VÁLIDA. VUELTA A INTENTARLO.")
                    print(" ")
                    print("¿ES FAVORITO? (S/N): ")
                    print(" ")
                    favorito = input("[>] ").lower()
            except ValueError:
                print("error")
        detalles_contacto = [{'categoria': categoria, 'direccion': direccion, 'telefono': telefono}]
        contacto = Contacto(nombre, edad, detalles_contacto, favorito)
        
        insertar_contacto(contacto)
        print("CONTACTO AGREGADO")


# Modificar contacto
    def modificar_contacto(self):
        self.limpiar()
        nombre = self.comprobar_texto("INGRESE EL NOMBRE DEL CONTACTO A MODIFICAR: ")
        contacto = coleccion_contactos.find_one({"nombre": nombre})
        if not contacto:
            print("EL CONTACTO NO SE ENCUENTRA EN LA BASE DE DATOS.")
            return
        
        detalles_contacto = contacto.get("detalles_contacto", [])
        # Validación de categoría para que pueda ser ingresada como texto o como número (string)
        while True:
            categoria_input = self.comprobar_texto("INGRESE LA CATEGORIA DE CONTACTO ([1] PARTICULAR, [2] COMERCIAL, [3] TRABAJO)")
            if categoria_input == "1":
                categoria = "particular"
            elif categoria_input == "2":
                categoria = "comercial"
            elif categoria_input == "3":
                categoria = "trabajo"
            else:
                categoria = categoria_input.lower()
                
            if categoria.lower() not in ["particular", "comercial", "trabajo"]:
                print("[!] DEBE INGRESAR UNA CATEGORIA. VUELTA A INTENTARLO.")
                continue
            direccion = self.comprobar_texto("INGRESE LA NUEVA DIRECCION: ")
            telefono = self.validar_entero("INGRESE EL NUEVO TELEFONO: ")
            break
        
        detalles_contacto.append({"categoria": categoria,"direccion": direccion,"telefono": telefono}) 
        
        modificar_contacto(nombre, detalles_contacto)
        print("CONTACTO MODIFICADO")

# Eliminar contacto
    def eliminar_contacto(self):
        self.limpiar()
        nombre = self.comprobar_texto("INGRESE EL NOMBRE DEL CONTACTO A ELIMINAR:  ")
        contacto = coleccion_contactos.find_one({"nombre": nombre})
        if not contacto:
            print("EL CONTACTO NO SE ENCUENTRA EN LA BASE DE DATOS.")
            return
        eliminar_contacto(nombre)
        print("CONTACTO ELIMINADO")
        
    def abrir_interfaz(self):
        while True:
            self.imprimir_menu()
            opcion = self.validar_entero()
            
            if opcion == 1:
                self.ingresar_contacto()

            elif opcion == 2:
                self.modificar_contacto()

            elif opcion == 3:
                self.eliminar_contacto()

            elif opcion == 4:
                self.limpiar()
                listar_contactos()

            elif opcion == 0:
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