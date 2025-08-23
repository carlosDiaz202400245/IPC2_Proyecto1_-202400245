class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

    def __str__(self):
        return str(self.dato)


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0

    def insertar(self, dato):
        """Inserta un nuevo elemento al final de la lista"""
        nuevo_nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.longitud += 1

    def esta_vacia(self):
        """Verifica si la lista está vacía"""
        return self.cabeza is None

    def recorrer(self):
        """Devuelve todos los elementos como una lista"""
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __iter__(self):
        """Iterador para la lista"""
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self):
        """Devuelve la longitud de la lista"""
        return self.longitud

    def buscar_por_id(self, id_buscar):
        """Busca un elemento por su atributo id"""
        actual = self.cabeza
        while actual is not None:
            if hasattr(actual.dato, 'id') and actual.dato.id == id_buscar:
                return actual.dato
            actual = actual.siguiente
        return None

    def obtener_por_indice(self, indice):
        """Obtiene el elemento en la posición especificada"""
        if indice < 0 or indice >= self.longitud:
            return None

        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual.dato

    def eliminar_por_id(self, id_eliminar):
        """Elimina un elemento por su atributo id"""
        if self.esta_vacia():
            return False

        # Caso especial: eliminar la cabeza
        if hasattr(self.cabeza.dato, 'id') and self.cabeza.dato.id == id_eliminar:
            self.cabeza = self.cabeza.siguiente
            self.longitud -= 1
            return True

        actual = self.cabeza
        anterior = None

        while actual is not None:
            if hasattr(actual.dato, 'id') and actual.dato.id == id_eliminar:
                anterior.siguiente = actual.siguiente
                self.longitud -= 1
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def __str__(self):
        """Representación en string de la lista"""
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return "[" + ", ".join(elementos) + "]"


class ParClaveValor:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor

    def __str__(self):
        return f"{self.clave}: {self.valor}"


class ListaPares:
    """Estructura personalizada para emular un diccionario"""

    def __init__(self):
        self.pares = ListaEnlazada()

    def insertar(self, clave, valor):
        """Inserta un par clave-valor"""
        # Primero verificar si la clave ya existe
        actual = self.pares.cabeza
        while actual is not None:
            if actual.dato.clave == clave:
                actual.dato.valor = valor  # Actualizar valor si existe
                return
            actual = actual.siguiente

        # Si no existe, insertar nuevo
        self.pares.insertar(ParClaveValor(clave, valor))

    def obtener(self, clave_buscar):
        """Obtiene el valor para una clave"""
        actual = self.pares.cabeza
        while actual is not None:
            if actual.dato.clave == clave_buscar:
                return actual.dato.valor
            actual = actual.siguiente
        return None

    def existe_clave(self, clave_buscar):
        """Verifica si una clave existe"""
        actual = self.pares.cabeza
        while actual is not None:
            if actual.dato.clave == clave_buscar:
                return True
            actual = actual.siguiente
        return False

    def eliminar(self, clave_eliminar):
        """Elimina un par clave-valor"""
        if self.pares.esta_vacia():
            return False

        # Caso especial: eliminar la cabeza
        if self.pares.cabeza.dato.clave == clave_eliminar:
            self.pares.cabeza = self.pares.cabeza.siguiente
            self.pares.longitud -= 1
            return True

        actual = self.pares.cabeza
        anterior = None

        while actual is not None:
            if actual.dato.clave == clave_eliminar:
                anterior.siguiente = actual.siguiente
                self.pares.longitud -= 1
                return True
            anterior = actual
            actual = actual.siguiente

        return False

    def obtener_todas_claves(self):
        """Obtiene todas las claves"""
        claves = []
        actual = self.pares.cabeza
        while actual is not None:
            claves.append(actual.dato.clave)
            actual = actual.siguiente
        return claves

    def obtener_todos_valores(self):
        """Obtiene todos los valores"""
        valores = []
        actual = self.pares.cabeza
        while actual is not None:
            valores.append(actual.dato.valor)
            actual = actual.siguiente
        return valores

    def __str__(self):
        """Representación en string de la lista de pares"""
        elementos = []
        actual = self.pares.cabeza
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        return "{" + ", ".join(elementos) + "}"


class Patron:
    """Clase para representar patrones sin usar tuplas nativas"""

    def __init__(self):
        self.valores = ListaEnlazada()

    def agregar_valor(self, valor):
        """Agrega un valor al patrón"""
        self.valores.insertar(valor)

    def es_igual(self, otro_patron):
        """Compara si dos patrones son iguales"""
        if otro_patron is None:
            return False
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

    def obtener_valores(self):
        """Obtiene los valores como lista"""
        valores = []
        actual = self.valores.cabeza
        while actual is not None:
            valores.append(actual.dato)
            actual = actual.siguiente
        return valores

    def __str__(self):
        """Representación en string del patrón"""
        valores = []
        actual = self.valores.cabeza
        while actual is not None:
            valores.append(str(actual.dato))
            actual = actual.siguiente
        return "[" + ", ".join(valores) + "]"

    def __len__(self):
        """Longitud del patrón"""
        return self.valores.longitud