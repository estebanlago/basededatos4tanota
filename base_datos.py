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
    
    for document in cursor:
        contacto_info = {
            "nombre": document.get('nombre'),
            "edad": document.get('edad'),
            "favorito": document.get('favorito'),
            "detalles_contacto": document.get('detalles_contacto', [])
        }
        lista_contactos.append(contacto_info)

    # La funcion sorted sirve para ordenar de forma descendente una lista, tupla, etc, se le agrega primero lo que se quiere ordenar 
    # en este caso "Lista_contactos", despues se le agrega el criterio con el cual se ordenará, se utiliza la funcion lambda x: x[criterio] 
    # en el criterio se le agrega el ['favorito'] para que retorne el true o el false, como sorted se ordena de forma descendente 
    # osea [6,5,4,3,2,1] tomará como false el primer puesto y true el ultimo, para revertir esto se le agrega un booleano llamado reverse 
    # el cual si está en True provoca que la informacion se liste de forma ascendente [1,2,3,4,5,6].
    lista_contactos = sorted(lista_contactos, key=lambda x: x['favorito'], reverse = True)

    cont = 0
    for contacto in lista_contactos:
        cont += 1
        print(" ")
        print(f"        [{cont}]  ")
        print(f"    Nombre: {contacto['nombre']}")
        print(f"    Edad: {contacto['edad']}")
        favorito = "Si" if contacto['favorito'] else "No"  #Operador Ternario: Variable = [Condicion si es True] if [variable] else [Condicion si es False]
        print(f"    Favorito: {favorito}")
        print(" ")
        print(" Detalles del Contacto:")
        print(" ")
        for detalle in contacto['detalles_contacto']:
            print(f"  Categoría: {detalle['categoria']}")
            print(f"  Dirección: {detalle['direccion']}")
            print(f"  Teléfono: {detalle['telefono']}")
            print("-----------------------------------")
