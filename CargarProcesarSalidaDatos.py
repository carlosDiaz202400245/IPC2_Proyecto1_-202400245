import xml.etree.ElementTree as ET
from EstructuraBase import ListaEnlazada, Patron
from Entidades import CampoAgricola, Estacion, SensorSuelo, SensorCultivo, GrupoEstaciones

def _lista_esta_vacia(lista_enlazada):
    """Verifica si una lista enlazada está vacía"""
    return lista_enlazada.cabeza is None


def _obtener_elementos_lista(lista_enlazada):
    """Convierte lista enlazada a lista normal para iteración"""
    elementos = []
    actual = lista_enlazada.cabeza
    while actual is not None:
        elementos.append(actual.dato)
        actual = actual.siguiente
    return elementos


def calcular_patrones_estaciones(campo):
    """Calcula los patrones binarios para cada estación usando nuestra clase Patron"""
    estaciones = _obtener_elementos_lista(campo.estaciones)
    sensores_suelo = _obtener_elementos_lista(campo.sensores_suelo)
    sensores_cultivo = _obtener_elementos_lista(campo.sensores_cultivo)

    for estacion in estaciones:
        # Patrón para sensores de suelo
        patron_suelo = Patron()
        for sensor in sensores_suelo:
            frecuencia = sensor.obtener_frecuencia(estacion.id)
            patron_suelo.agregar_valor(1 if frecuencia > 0 else 0)
        estacion.patron_suelo = patron_suelo

        # Patrón para sensores de cultivo
        patron_cultivo = Patron()
        for sensor in sensores_cultivo:
            frecuencia = sensor.obtener_frecuencia(estacion.id)
            patron_cultivo.agregar_valor(1 if frecuencia > 0 else 0)
        estacion.patron_cultivo = patron_cultivo


def patrones_iguales(patron1, patron2):
    """Compara si dos patrones son iguales usando nuestra implementación"""
    if patron1 is None or patron2 is None:
        return False
    return patron1.es_igual(patron2)


class GrupoPatron:
    """Clase para agrupar estaciones por patrones similares"""

    def __init__(self, patron_suelo, patron_cultivo):
        self.patron_suelo = patron_suelo
        self.patron_cultivo = patron_cultivo
        self.estaciones = ListaEnlazada()

    def agregar_estacion(self, estacion):
        self.estaciones.insertar(estacion)

    def tiene_mismos_patrones(self, patron_suelo, patron_cultivo):
        """Verifica si los patrones coinciden"""
        return (patrones_iguales(self.patron_suelo, patron_suelo) and
                patrones_iguales(self.patron_cultivo, patron_cultivo))


def agrupar_estaciones_comparacion_directa(campo):
    """
    Algoritmo corregido para agrupar estaciones por patrones similares
    """
    # Obtener todas las estaciones
    todas_estaciones = []
    actual = campo.estaciones.cabeza
    while actual is not None:
        todas_estaciones.append(actual.dato)
        actual = actual.siguiente

    # Lista para grupos finales
    grupos_finales = ListaEnlazada()
    estaciones_procesadas = set()

    for i, estacion_actual in enumerate(todas_estaciones):
        if estacion_actual.id in estaciones_procesadas:
            continue

        # Crear nuevo grupo con esta estación
        estaciones_grupo = [estacion_actual]
        estaciones_procesadas.add(estacion_actual.id)

        # Buscar estaciones con los mismos patrones
        for j in range(i + 1, len(todas_estaciones)):
            estacion_comparar = todas_estaciones[j]

            if estacion_comparar.id in estaciones_procesadas:
                continue

            # Comparar patrones
            patrones_iguales_suelo = patrones_iguales(
                estacion_actual.patron_suelo,
                estacion_comparar.patron_suelo
            )
            patrones_iguales_cultivo = patrones_iguales(
                estacion_actual.patron_cultivo,
                estacion_comparar.patron_cultivo
            )

            if patrones_iguales_suelo and patrones_iguales_cultivo:
                estaciones_grupo.append(estacion_comparar)
                estaciones_procesadas.add(estacion_comparar.id)

        # Crear objeto GrupoEstaciones
        if estaciones_grupo:
            grupo_obj = GrupoEstaciones(estaciones_grupo)
            grupos_finales.insertar(grupo_obj)

    return grupos_finales


def procesar_campo(campo):
    print(f"➢ Procesando campo {campo.id}")

    # Calcular patrones para cada estación
    calcular_patrones_estaciones(campo)

    # Agrupar estaciones por patrones similares
    agrupar_estaciones_comparacion_directa(campo)

    # Contar estaciones y grupos
    num_estaciones = 0
    actual = campo.estaciones.cabeza
    while actual is not None:
        num_estaciones += 1
        actual = actual.siguiente

    num_grupos = 0
    actual = campo.grupos_estaciones.cabeza
    while actual is not None:
        num_grupos += 1
        actual = actual.siguiente

    print(f"➢ Campo {campo.id} procesado exitosamente")
    print(f"➢ Estaciones originales: {num_estaciones}")
    print(f"➢ Grupos reducidos: {num_grupos}")


def generar_xml_salida(campos, ruta_salida):
    try:
        root = ET.Element('camposAgricolas')

        actual_campo = campos.cabeza
        while actual_campo is not None:
            campo = actual_campo.dato
            campo_xml = ET.SubElement(root, 'campo', id=campo.id, nombre=campo.nombre)

            # Estaciones base reducidas
            estaciones_reducidas_xml = ET.SubElement(campo_xml, 'estacionesBaseReducidas')

            actual_grupo = campo.grupos_estaciones.cabeza
            while actual_grupo is not None:
                grupo = actual_grupo.dato
                ET.SubElement(estaciones_reducidas_xml, 'estacion',
                              id=grupo.id_representante,
                              nombre=grupo.nombre_representante)
                actual_grupo = actual_grupo.siguiente

            # Sensores de suelo con frecuencias reducidas
            sensores_suelo_xml = ET.SubElement(campo_xml, 'sensoresSuelo')

            actual_sensor = campo.sensores_suelo.cabeza
            while actual_sensor is not None:
                sensor = actual_sensor.dato
                sensor_xml = ET.SubElement(sensores_suelo_xml, 'sensor',
                                           id=sensor.id, nombre=sensor.nombre)

                actual_grupo = campo.grupos_estaciones.cabeza
                while actual_grupo is not None:
                    grupo = actual_grupo.dato
                    frecuencia_total = 0

                    actual_estacion = grupo.estaciones.cabeza
                    while actual_estacion is not None:
                        estacion = actual_estacion.dato
                        frecuencia_total += sensor.obtener_frecuencia(estacion.id)
                        actual_estacion = actual_estacion.siguiente

                    if frecuencia_total > 0:
                        frecuencia_elem = ET.SubElement(sensor_xml, 'frecuencia')
                        frecuencia_elem.set('idEstacion', grupo.id_representante)
                        frecuencia_elem.text = str(frecuencia_total)

                    actual_grupo = actual_grupo.siguiente

                actual_sensor = actual_sensor.siguiente

            # Sensores de cultivo con frecuencias reducidas
            sensores_cultivo_xml = ET.SubElement(campo_xml, 'sensoresCultivo')

            actual_sensor = campo.sensores_cultivo.cabeza
            while actual_sensor is not None:
                sensor = actual_sensor.dato
                sensor_xml = ET.SubElement(sensores_cultivo_xml, 'sensorT',
                                           id=sensor.id, nombre=sensor.nombre)

                actual_grupo = campo.grupos_estaciones.cabeza
                while actual_grupo is not None:
                    grupo = actual_grupo.dato
                    frecuencia_total = 0

                    actual_estacion = grupo.estaciones.cabeza
                    while actual_estacion is not None:
                        estacion = actual_estacion.dato
                        frecuencia_total += sensor.obtener_frecuencia(estacion.id)
                        actual_estacion = actual_estacion.siguiente

                    if frecuencia_total > 0:
                        frecuencia_elem = ET.SubElement(sensor_xml, 'frecuencia')
                        frecuencia_elem.set('idEstacion', grupo.id_representante)
                        frecuencia_elem.text = str(frecuencia_total)

                    actual_grupo = actual_grupo.siguiente

                actual_sensor = actual_sensor.siguiente

            actual_campo = actual_campo.siguiente

        # Formatear y guardar el XML
        ET.indent(root, space="    ", level=0)
        tree = ET.ElementTree(root)
        tree.write(ruta_salida, encoding='utf-8', xml_declaration=True)

        print(f"➢ Archivo de salida generado en: {ruta_salida}")
        return True

    except Exception as e:
        print(f"❌ Error al generar archivo de salida: {e}")
        return False