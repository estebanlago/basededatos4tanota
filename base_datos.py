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
    return list(coleccion_contactos.find({}).sort('favorito', -1))
