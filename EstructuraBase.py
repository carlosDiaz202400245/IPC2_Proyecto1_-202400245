class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0

    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.longitud += 1

    def recorrer(self):
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def buscar_por_id(self, id_buscar):
        actual = self.cabeza
        while actual is not None:
            if hasattr(actual.dato, 'id') and actual.dato.id == id_buscar:
                return actual.dato
            actual = actual.siguiente
        return None

    def esta_vacia(self):
        return self.cabeza is None


class ParClaveValor:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor


class ListaPares:
    """Estructura personalizada para emular un diccionario"""
    def __init__(self):
        self.pares = ListaEnlazada()

    def insertar(self, clave, valor):
        self.pares.insertar(ParClaveValor(clave, valor))

    def obtener(self, clave_buscar):
        for par in self.pares:
            if par.clave == clave_buscar:
                return par.valor
        return None

    def existe_clave(self, clave_buscar):
        for par in self.pares:
            if par.clave == clave_buscar:
                return True
        return False

    def obtener_todas_claves(self):
        claves = []
        for par in self.pares:
            claves.append(par.clave)
        return claves

    def obtener_todos_valores(self):
        valores = []
        for par in self.pares:
            valores.append(par.valor)
        return valores


class Patron:
    """Clase para representar patrones sin usar tuplas nativas"""
    def __init__(self):
        self.valores = ListaEnlazada()

    def agregar_valor(self, valor):
        self.valores.insertar(valor)

    def es_igual(self, otro_patron):
        """Compara si dos patrones son iguales"""
        if self.valores.longitud != otro_patron.valores.longitud:
            return False

        actual1 = self.valores.cabeza
        actual2 = otro_patron.valores.cabeza

        while actual1 is not None and actual2 is not None:
            if actual1.dato != actual2.dato:
                return False
            actual1 = actual1.siguiente
            actual2 = actual2.siguiente

        return True

    def clonar(self):
        """Crea una copia del patrón"""
        nuevo_patron = Patron()
        actual = self.valores.cabeza
        while actual is not None:
            nuevo_patron.agregar_valor(actual.dato)
            actual = actual.siguiente
        return nuevo_patron

    def __str__(self):
        valores = []
        actual = self.valores.cabeza
        while actual is not None:
            valores.append(str(actual.dato))
            actual = actual.siguiente
        return "[" + ", ".join(valores) + "]"