from EstructuraBase import ListaEnlazada

class Estacion:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class SensorSuelo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaEnlazada()  # Almacenamos objetos de frecuencia pa

class Frecuencia:
    def __init__(self, id_estacion, valor):
        self.id_estacion = id_estacion
        self.valor = valor