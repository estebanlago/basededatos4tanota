from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017/')
bd = cliente['agenda']
coleccion_contactos = bd['contactos']

def insertar_contacto(contacto):
    coleccion_contactos.insert_one(contacto.__dict__)

def modificar_contacto(nombre, detalles_contacto):
    # no estoy seguro si pide $set o {"$push": {"detalles_contacto": nuevos_detalles}}
    coleccion_contactos.update_one({'nombre': nombre}, {'$set': {"detalles_contacto": detalles_contacto} })

def eliminar_contacto(nombre):
    coleccion_contactos.delete_one({'nombre': nombre})

def listar_contactos():
    cursor = coleccion_contactos.find()
    lista_contactos = []
    cont = 0

    for document in cursor:
        contacto_info = {
            "nombre": document.get('nombre'),
            "edad": document.get('edad'),
            "favorito": document.get('favorito'),
            "detalles_contacto": document.get('detalles_contacto', [])
        }

        # Agregar el contacto a la lista de contactos jeje
        lista_contactos.append(contacto_info)

    # Este ciclo muestra los contactos
    for contacto in lista_contactos:
        cont = cont + 1
        print(" ")
        print(f"        [{cont}]  ")
        print(f"    Nombre: {contacto['nombre']}")
        print(f"    Edad: {contacto['edad']}")
        if contacto['favorito'] == True:
            contacto['favorito'] = "Si"
        else:
            contacto['favorito'] = "No"
        print(f"    Favorito: {contacto['favorito']}")
        print(" ")
        print(" Detalles del Contacto:")
        print(" ")
        for detalle in contacto['detalles_contacto']:
            print(f"  Categoría: {detalle['categoria']}")
            print(f"  Dirección: {detalle['direccion']}")
            print(f"  Teléfono: {detalle['telefono']}")
            print("-----------------------------------")

