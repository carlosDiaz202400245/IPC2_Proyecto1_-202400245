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
            os.makedirs(os.path.dirname(nombre_archivo) if os.path.dirname(nombre_archivo) else None, exist_ok=True)

            dot.render(nombre_archivo, format='png', cleanup=True)
            print(f"✅ Gráfica {tipo_matriz} generada: {nombre_archivo}.png")
            return True

        except Exception as e:
            print(f"❌ Error al generar gráfica: {e}")
            return False

    def _graficar_matriz_frecuencias(self, dot, campo):
        """Genera gráfica de matriz de frecuencias originales"""
        dot.attr(label=f'Matriz de Frecuencias - Campo {campo.nombre}\n\n')

        # Tabla HTML para mejor formato
        tabla_html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightblue"><B>Estación/Sensor</B></TD>'''

        # Encabezados de sensores de suelo
        sensores_suelo = []
        actual_sensor = campo.sensores_suelo.cabeza
        while actual_sensor is not None:
            sensores_suelo.append(actual_sensor.dato)
            tabla_html += f'<TD BGCOLOR="lightgreen"><B>{actual_sensor.dato.id}</B></TD>'
            actual_sensor = actual_sensor.siguiente

        # Encabezados de sensores de cultivo
        sensores_cultivo = []
        actual_sensor = campo.sensores_cultivo.cabeza
        while actual_sensor is not None:
            sensores_cultivo.append(actual_sensor.dato)
            tabla_html += f'<TD BGCOLOR="lightyellow"><B>{actual_sensor.dato.id}</B></TD>'
            actual_sensor = actual_sensor.siguiente

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

        # Primero calcular patrones si no están calculados
        from CargarProcesarSalidaDatos import calcular_patrones_estaciones
        calcular_patrones_estaciones(campo)

        tabla_html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightblue"><B>Estación/Sensor</B></TD>'''

        # Encabezados de sensores
        sensores_suelo = []
        actual_sensor = campo.sensores_suelo.cabeza
        while actual_sensor is not None:
            sensores_suelo.append(actual_sensor.dato)
            tabla_html += f'<TD BGCOLOR="lightgreen"><B>{actual_sensor.dato.id}</B></TD>'
            actual_sensor = actual_sensor.siguiente

        sensores_cultivo = []
        actual_sensor = campo.sensores_cultivo.cabeza
        while actual_sensor is not None:
            sensores_cultivo.append(actual_sensor.dato)
            tabla_html += f'<TD BGCOLOR="lightyellow"><B>{actual_sensor.dato.id}</B></TD>'
            actual_sensor = actual_sensor.siguiente

        tabla_html += '</TR>'

        # Filas para cada estación
        actual_estacion = campo.estaciones.cabeza
        while actual_estacion is not None:
            estacion = actual_estacion.dato
            tabla_html += f'<TR><TD BGCOLOR="lightblue"><B>{estacion.id}</B></TD>'

            # Valores de patrones de suelo
            if estacion.patron_suelo:
                actual_valor = estacion.patron_suelo.valores.cabeza
                sensor_count = 0
                while actual_valor is not None and sensor_count < len(sensores_suelo):
                    valor = actual_valor.dato
                    color = "red" if valor == 0 else "green"
                    texto = "0" if valor == 0 else "1"
                    tabla_html += f'<TD BGCOLOR="{color}"><FONT COLOR="white">{texto}</FONT></TD>'
                    actual_valor = actual_valor.siguiente
                    sensor_count += 1

            # Valores de patrones de cultivo
            if estacion.patron_cultivo:
                actual_valor = estacion.patron_cultivo.valores.cabeza
                sensor_count = 0
                while actual_valor is not None and sensor_count < len(sensores_cultivo):
                    valor = actual_valor.dato
                    color = "red" if valor == 0 else "green"
                    texto = "0" if valor == 0 else "1"
                    tabla_html += f'<TD BGCOLOR="{color}"><FONT COLOR="white">{texto}</FONT></TD>'
                    actual_valor = actual_valor.siguiente
                    sensor_count += 1

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

        tabla_html = '''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="lightblue"><B>Grupo/Sensor</B></TD>'''

        # Encabezados de sensores
        sensores_suelo = []
        actual_sensor = campo.sensores_suelo.cabeza
        while actual_sensor is not None:
            sensores_suelo.append(actual_sensor.dato)
            tabla_html += f'<TD BGCOLOR="lightgreen"><B>{actual_sensor.dato.id}</B></TD>'
            actual_sensor = actual_sensor.siguiente

        sensores_cultivo = []
        actual_sensor = campo.sensores_cultivo.cabeza
        while actual_sensor is not None:
            sensores_cultivo.append(actual_sensor.dato)
            tabla_html += f'<TD BGCOLOR="lightyellow"><B>{actual_sensor.dato.id}</B></TD>'
            actual_sensor = actual_sensor.siguiente

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