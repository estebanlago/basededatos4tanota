from pymongo import MongoClient

cliente = MongoClient('mongodb://localhost:27017/')
bd = cliente['agenda']
coleccion_contactos = bd['contactos']

def insertar_contacto(contacto):
    coleccion_contactos.insert_one(contacto.__dict__)

def modificar_contacto(nombre, nuevos_detalles):
    coleccion_contactos.update_one({'nombre': nombre}, {'$set': nuevos_detalles})

def eliminar_contacto(nombre):
    coleccion_contactos.delete_one({'nombre': nombre})

def listar_contactos():
    lista_contactos = []
    cursor = coleccion_contactos.find()
    cont=0

    for document in cursor:
        lista_contactos = []
    cursor = coleccion_contactos.find()
    
    for document in cursor:
<<<<<<< HEAD
=======
        cont= cont+1
        print(f"""              [{cont}]""")
>>>>>>> badd5eb88f00055534c26dd62bbe149b9b613c98
        nombre = document.get("nombre", "")
        edad = document.get("edad", "")
        favorito = document.get("favorito", False)
        detalles_contacto = document.get("detalles_contacto", [])

        for contacto in detalles_contacto:
            telefono = contacto.get("telefono", "")
            direccion = contacto.get("direccion", "")
            categoria = contacto.get("categoria", "")
        
            lista_contactos.append({
                "nombre": nombre,
                "edad": edad,
                "favorito": favorito,
                "telefono": telefono,
                "direccion": direccion,
                "categoria": categoria.lower(),
            })

    for dato in lista_contactos:
<<<<<<< HEAD
        cont= cont+1
        print(f"""              [{cont}]""")
=======
>>>>>>> badd5eb88f00055534c26dd62bbe149b9b613c98
        print(f"Nombre: {dato['nombre']}")
        print(f"Edad: {dato['edad']}")
        print(f"Favorito: {dato['favorito']}")
        print(f"Telefono: {dato['telefono']}")
        print(f"Direccion: {dato['direccion']}")
        print(f"Categoria: {dato['categoria']}")
        print("-" * 20)
    
