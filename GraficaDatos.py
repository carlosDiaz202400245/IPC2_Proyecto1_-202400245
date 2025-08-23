from graphviz import Digraph
import os


class GraficadoraDatos:
    def __init__(self):
        pass

    def generar_grafica(self, campo, tipo_matriz, nombre_archivo):
        """Método principal para generar gráficas"""
        try:
            dot = Digraph(comment=f'Matriz {tipo_matriz} - Campo {campo.id}')
            dot.attr(rankdir='TB')  # Top to Bottom orientation

            if tipo_matriz == "frecuencias":
                self._graficar_matriz_frecuencias(dot, campo)
            elif tipo_matriz == "patrones":
                self._graficar_matriz_patrones(dot, campo)
            elif tipo_matriz == "reducida":
                self._graficar_matriz_reducida(dot, campo)
            else:
                print("❌ Tipo de matriz no válido")
                return False

            # Asegurar que la ruta existe
            if os.path.dirname(nombre_archivo):
                os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

            dot.render(nombre_archivo, format='png', cleanup=True)
            print(f"✅ Gráfica {tipo_matriz} generada: {nombre_archivo}.png")
            return True

        except Exception as e:
            print(f"❌ Error al generar gráfica: {e}")
            return False

    def _contar_sensores(self, lista_sensores):
        """Cuenta la cantidad de sensores en una lista enlazada"""
        count = 0
        actual = lista_sensores.cabeza
        while actual is not None:
            count += 1
            actual = actual.siguiente
        return count

    def _obtener_lista_sensores(self, lista_sensores):
        """Convierte lista enlazada a lista normal para iteración"""
        sensores = []
        actual = lista_sensores.cabeza
        while actual is not None:
            sensores.append(actual.dato)
            actual = actual.siguiente
        return sensores

    def _obtener_valores_patron(self, patron):
        """Obtiene los valores de un patrón como lista"""
        valores = []
        if patron and hasattr(patron, 'valores'):
            actual = patron.valores.cabeza
            while actual is not None:
                valores.append(actual.dato)
                actual = actual.siguiente
        return valores

    def _graficar_matriz_frecuencias(self, dot, campo):
        """Genera gráfica de matriz de frecuencias originales"""
        dot.attr(label=f'Matriz de Frecuencias - Campo {campo.nombre}\n\n')

        # Obtener listas de sensores
        sensores_suelo = self._obtener_lista_sensores(campo.sensores_suelo)
        sensores_cultivo = self._obtener_lista_sensores(campo.sensores_cultivo)

        # Tabla HTML para mejor formato
        tabla_html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightblue"><B>Estación/Sensor</B></TD>'''

        # Encabezados de sensores de suelo
        for sensor in sensores_suelo:
            tabla_html += f'<TD BGCOLOR="lightgreen"><B>{sensor.id}</B></TD>'

        # Encabezados de sensores de cultivo
        for sensor in sensores_cultivo:
            tabla_html += f'<TD BGCOLOR="lightyellow"><B>{sensor.id}</B></TD>'

        tabla_html += '</TR>'

        # Filas para cada estación
        actual_estacion = campo.estaciones.cabeza
        while actual_estacion is not None:
            estacion = actual_estacion.dato
            tabla_html += f'<TR><TD BGCOLOR="lightblue"><B>{estacion.id}</B></TD>'

            # Valores para sensores de suelo
            for sensor in sensores_suelo:
                frecuencia = sensor.obtener_frecuencia(estacion.id)
                color = "white" if frecuencia == 0 else "palegreen"
                tabla_html += f'<TD BGCOLOR="{color}">{frecuencia}</TD>'

            # Valores para sensores de cultivo
            for sensor in sensores_cultivo:
                frecuencia = sensor.obtener_frecuencia(estacion.id)
                color = "white" if frecuencia == 0 else "lightyellow"
                tabla_html += f'<TD BGCOLOR="{color}">{frecuencia}</TD>'

            tabla_html += '</TR>'
            actual_estacion = actual_estacion.siguiente

        tabla_html += '</TABLE>>'

        dot.node('matriz', label=tabla_html, shape='none')

    def _graficar_matriz_patrones(self, dot, campo):
        """Genera gráfica de matriz de patrones binarios"""
        dot.attr(label=f'Matriz de Patrones - Campo {campo.nombre}\n\n')

        # Calcular patrones si no están calculados
        if not hasattr(campo.estaciones.cabeza.dato,
                       'patron_suelo') or campo.estaciones.cabeza.dato.patron_suelo is None:
            try:
                from CargarProcesarSalidaDatos import calcular_patrones_estaciones
                calcular_patrones_estaciones(campo)
            except ImportError:
                print("❌ No se pudo importar calcular_patrones_estaciones")
                return

        # Obtener listas de sensores
        sensores_suelo = self._obtener_lista_sensores(campo.sensores_suelo)
        sensores_cultivo = self._obtener_lista_sensores(campo.sensores_cultivo)

        total_sensores = len(sensores_suelo) + len(sensores_cultivo)

        tabla_html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightblue"><B>Estación/Sensor</B></TD>'''

        # Encabezados de sensores
        for sensor in sensores_suelo:
            tabla_html += f'<TD BGCOLOR="lightgreen"><B>{sensor.id}</B></TD>'

        for sensor in sensores_cultivo:
            tabla_html += f'<TD BGCOLOR="lightyellow"><B>{sensor.id}</B></TD>'

        tabla_html += '</TR>'

        # Filas para cada estación
        actual_estacion = campo.estaciones.cabeza
        while actual_estacion is not None:
            estacion = actual_estacion.dato
            tabla_html += f'<TR><TD BGCOLOR="lightblue"><B>{estacion.id}</B></TD>'

            # Valores de patrones
            valores_suelo = self._obtener_valores_patron(estacion.patron_suelo)
            valores_cultivo = self._obtener_valores_patron(estacion.patron_cultivo)

            # Patrones de suelo
            for i in range(len(sensores_suelo)):
                valor = valores_suelo[i] if i < len(valores_suelo) else 0
                color = "red" if valor == 0 else "green"
                texto = "0" if valor == 0 else "1"
                tabla_html += f'<TD BGCOLOR="{color}"><FONT COLOR="white">{texto}</FONT></TD>'

            # Patrones de cultivo
            for i in range(len(sensores_cultivo)):
                valor = valores_cultivo[i] if i < len(valores_cultivo) else 0
                color = "red" if valor == 0 else "green"
                texto = "0" if valor == 0 else "1"
                tabla_html += f'<TD BGCOLOR="{color}"><FONT COLOR="white">{texto}</FONT></TD>'

            tabla_html += '</TR>'
            actual_estacion = actual_estacion.siguiente

        tabla_html += '</TABLE>>'

        dot.node('matriz_patrones', label=tabla_html, shape='none')

    def _graficar_matriz_reducida(self, dot, campo):
        """Genera gráfica de matriz reducida después del agrupamiento"""
        dot.attr(label=f'Matriz Reducida - Campo {campo.nombre}\n\n')

        if campo.grupos_estaciones.esta_vacia():
            dot.node('error', label='No hay grupos reducidos. Ejecute "Procesar archivo" primero.', shape='box')
            return

        # Obtener listas de sensores
        sensores_suelo = self._obtener_lista_sensores(campo.sensores_suelo)
        sensores_cultivo = self._obtener_lista_sensores(campo.sensores_cultivo)

        tabla_html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightblue"><B>Grupo/Sensor</B></TD>'''

        # Encabezados de sensores
        for sensor in sensores_suelo:
            tabla_html += f'<TD BGCOLOR="lightgreen"><B>{sensor.id}</B></TD>'

        for sensor in sensores_cultivo:
            tabla_html += f'<TD BGCOLOR="lightyellow"><B>{sensor.id}</B></TD>'

        tabla_html += '</TR>'

        # Filas para cada grupo
        actual_grupo = campo.grupos_estaciones.cabeza
        while actual_grupo is not None:
            grupo = actual_grupo.dato
            tabla_html += f'<TR><TD BGCOLOR="lightblue"><B>{grupo.id_representante}</B></TD>'

            # Valores para sensores de suelo
            for sensor in sensores_suelo:
                frecuencia_total = 0
                actual_estacion = grupo.estaciones.cabeza
                while actual_estacion is not None:
                    estacion = actual_estacion.dato
                    frecuencia_total += sensor.obtener_frecuencia(estacion.id)
                    actual_estacion = actual_estacion.siguiente

                color = "white" if frecuencia_total == 0 else "palegreen"
                tabla_html += f'<TD BGCOLOR="{color}">{frecuencia_total}</TD>'

            # Valores para sensores de cultivo
            for sensor in sensores_cultivo:
                frecuencia_total = 0
                actual_estacion = grupo.estaciones.cabeza
                while actual_estacion is not None:
                    estacion = actual_estacion.dato
                    frecuencia_total += sensor.obtener_frecuencia(estacion.id)
                    actual_estacion = actual_estacion.siguiente

                color = "white" if frecuencia_total == 0 else "lightyellow"
                tabla_html += f'<TD BGCOLOR="{color}">{frecuencia_total}</TD>'

            tabla_html += '</TR>'
            actual_grupo = actual_grupo.siguiente

        tabla_html += '</TABLE>>'

        dot.node('matriz_reducida', label=tabla_html, shape='none')