from EstructuraBase import ListaEnlazada


class Frecuencia:
    def __init__(self, id_estacion, valor):
        self.id_estacion = id_estacion
        self.valor = valor

    def __str__(self):
        return f"Frecuencia para estación {self.id_estacion}: {self.valor}"


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
        frecuencia = Frecuencia(id_estacion, valor)
        self.frecuencias.insertar(frecuencia)

    def obtener_frecuencia(self, id_estacion):
        """Obtiene la frecuencia de forma eficiente para lista enlazada"""
        actual = self.frecuencias.cabeza
        while actual is not None:
            if actual.dato.id_estacion == id_estacion:
                return actual.dato.valor
            actual = actual.siguiente
        return 0

    def __str__(self):
        return f"Sensor Suelo {self.id}: {self.nombre}"


class SensorCultivo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaEnlazada()

    def agregar_frecuencia(self, id_estacion, valor):
        frecuencia = Frecuencia(id_estacion, valor)
        self.frecuencias.insertar(frecuencia)

    def obtener_frecuencia(self, id_estacion):
        """Obtiene la frecuencia de forma eficiente para lista enlazada"""
        actual = self.frecuencias.cabeza
        while actual is not None:
            if actual.dato.id_estacion == id_estacion:
                return actual.dato.valor
            actual = actual.siguiente
        return 0

    def __str__(self):
        return f"Sensor Cultivo {self.id}: {self.nombre}"


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

    def obtener_estacion_por_id(self, id_estacion):
        """Obtiene una estación por su ID"""
        actual = self.estaciones.cabeza
        while actual is not None:
            if actual.dato.id == id_estacion:
                return actual.dato
            actual = actual.siguiente
        return None

    def obtener_sensor_suelo_por_id(self, id_sensor):
        """Obtiene un sensor de suelo por su ID"""
        actual = self.sensores_suelo.cabeza
        while actual is not None:
            if actual.dato.id == id_sensor:
                return actual.dato
            actual = actual.siguiente
        return None

    def obtener_sensor_cultivo_por_id(self, id_sensor):
        """Obtiene un sensor de cultivo por su ID"""
        actual = self.sensores_cultivo.cabeza
        while actual is not None:
            if actual.dato.id == id_sensor:
                return actual.dato
            actual = actual.siguiente
        return None

    def __str__(self):
        return f"Campo {self.id}: {self.nombre}"


class GrupoEstaciones:
    def __init__(self, estaciones):
        # Convertir a lista si es una ListaEnlazada
        if isinstance(estaciones, ListaEnlazada):
            self.estaciones_lista = self._convertir_lista_enlazada(estaciones)
        else:
            self.estaciones_lista = estaciones

        self.id_representante = self.estaciones_lista[0].id if self.estaciones_lista else ""

        # Construir nombre concatenado
        nombres = []
        for estacion in self.estaciones_lista:
            nombres.append(estacion.nombre)
        self.nombre_representante = ", ".join(nombres)

    def _convertir_lista_enlazada(self, lista_enlazada):
        """Convierte ListaEnlazada a lista normal"""
        elementos = []
        actual = lista_enlazada.cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def obtener_frecuencia_total(self, sensor, tipo_sensor):
        total = 0
        for estacion in self.estaciones_lista:
            if tipo_sensor == "suelo":
                total += sensor.obtener_frecuencia(estacion.id)
            else:  # cultivo
                total += sensor.obtener_frecuencia(estacion.id)
        return total

    def __str__(self):
        return f"GrupoEstaciones[{self.id_representante}]: {self.nombre_representante}"

    def __iter__(self):
        """Iterador para las estaciones del grupo"""
        return iter(self.estaciones_lista)

    def __len__(self):
        """Número de estaciones en el grupo"""
        return len(self.estaciones_lista)