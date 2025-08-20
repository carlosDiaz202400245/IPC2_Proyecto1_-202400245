from EstructuraBase import ListaEnlazada


class Estacion:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.patron_suelo = None
        self.patron_cultivo = None

    def __str__(self):
        return f"Estacion {self.id}: {self.nombre}"


class SensorSuelo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaEnlazada()

    def agregar_frecuencia(self, id_estacion, valor):
        from ClasesPrincipales import Frecuencia
        frecuencia = Frecuencia(id_estacion, valor)
        self.frecuencias.insertar(frecuencia)

    def obtener_frecuencia(self, id_estacion):
        for frecuencia in self.frecuencias:
            if frecuencia.id_estacion == id_estacion:
                return frecuencia.valor
        return 0

    def __str__(self):
        return f"Sensor Suelo {self.id}: {self.nombre}"


class SensorCultivo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaEnlazada()

    def agregar_frecuencia(self, id_estacion, valor):
        from ClasesPrincipales import Frecuencia
        frecuencia = Frecuencia(id_estacion, valor)
        self.frecuencias.insertar(frecuencia)

    def obtener_frecuencia(self, id_estacion):
        for frecuencia in self.frecuencias:
            if frecuencia.id_estacion == id_estacion:
                return frecuencia.valor
        return 0

    def __str__(self):
        return f"Sensor Cultivo {self.id}: {self.nombre}"


class Frecuencia:
    def __init__(self, id_estacion, valor):
        self.id_estacion = id_estacion
        self.valor = valor

    def __str__(self):
        return f"Frecuencia para estación {self.id_estacion}: {self.valor}"


class CampoAgricola:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = ListaEnlazada()
        self.sensores_suelo = ListaEnlazada()
        self.sensores_cultivo = ListaEnlazada()
        self.grupos_estaciones = ListaEnlazada()

    def agregar_estacion(self, estacion):
        self.estaciones.insertar(estacion)

    def agregar_sensor_suelo(self, sensor):
        self.sensores_suelo.insertar(sensor)

    def agregar_sensor_cultivo(self, sensor):
        self.sensores_cultivo.insertar(sensor)

    def __str__(self):
        return f"Campo {self.id}: {self.nombre}"


class GrupoEstaciones:
    def __init__(self, estaciones):
        self.estaciones = estaciones
        self.id_representante = estaciones[0].id if estaciones else ""

        # Construir nombre concatenado manualmente
        nombres = []
        for estacion in estaciones:
            nombres.append(estacion.nombre)
        self.nombre_representante = ", ".join(nombres)

    def obtener_frecuencia_total(self, sensor, tipo_sensor):
        total = 0
        for estacion in self.estaciones:
            if tipo_sensor == "suelo":
                total += sensor.obtener_frecuencia(estacion.id)
            else:  # cultivo
                total += sensor.obtener_frecuencia(estacion.id)
        return total