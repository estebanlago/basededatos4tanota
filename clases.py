# favorito = False para definir que es un booleano y por defecto es falso (no)
class Contacto:
    def __init__(self, nombre, edad, detalles_contacto, favorito=False):
        self.nombre = nombre
        self.edad = edad
        self.detalles_contacto = detalles_contacto  
        self.favorito = favorito
