import xml.etree.ElementTree as ET
from EstructuraBase import ListaEnlazada, Patron
from ClasesPrincipales import CampoAgricola, Estacion, SensorSuelo, SensorCultivo, GrupoEstaciones


def calcular_patrones_estaciones(campo):
    """Calcula los patrones binarios para cada estación usando nuestra clase Patron"""
    for estacion in campo.estaciones:
        # Patrón para sensores de suelo
        patron_suelo = Patron()
        for sensor in campo.sensores_suelo:
            frecuencia = sensor.obtener_frecuencia(estacion.id)
            patron_suelo.agregar_valor(1 if frecuencia > 0 else 0)
        estacion.patron_suelo = patron_suelo

        # Patrón para sensores de cultivo
        patron_cultivo = Patron()
        for sensor in campo.sensores_cultivo:
            frecuencia = sensor.obtener_frecuencia(estacion.id)
            patron_cultivo.agregar_valor(1 if frecuencia > 0 else 0)
        estacion.patron_cultivo = patron_cultivo


def patrones_iguales(patron1, patron2):
    """Compara si dos patrones son iguales usando nuestra implementación"""
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
        return (self.patron_suelo.es_igual(patron_suelo) and
                self.patron_cultivo.es_igual(patron_cultivo))


def agrupar_estaciones_sin_estructuras_nativas(campo):
    """Agrupa estaciones sin usar estructuras nativas de Python"""
    grupos_patron = ListaEnlazada()

    for estacion in campo.estaciones:
        encontrado = False

        # Buscar si ya existe un grupo con los mismos patrones
        actual_grupo = grupos_patron.cabeza
        while actual_grupo is not None:
            grupo = actual_grupo.dato
            if grupo.tiene_mismos_patrones(estacion.patron_suelo, estacion.patron_cultivo):
                grupo.agregar_estacion(estacion)
                encontrado = True
                break
            actual_grupo = actual_grupo.siguiente

        if not encontrado:
            # Crear nuevo grupo
            nuevo_grupo = GrupoPatron(
                estacion.patron_suelo.clonar(),
                estacion.patron_cultivo.clonar()
            )
            nuevo_grupo.agregar_estacion(estacion)
            grupos_patron.insertar(nuevo_grupo)

    # Convertir a objetos GrupoEstaciones
    actual_grupo = grupos_patron.cabeza
    while actual_grupo is not None:
        grupo_patron = actual_grupo.dato
        estaciones_grupo = []

        actual_estacion = grupo_patron.estaciones.cabeza
        while actual_estacion is not None:
            estaciones_grupo.append(actual_estacion.dato)
            actual_estacion = actual_estacion.siguiente

        if estaciones_grupo:
            grupo_obj = GrupoEstaciones(estaciones_grupo)
            campo.grupos_estaciones.insertar(grupo_obj)

        actual_grupo = actual_grupo.siguiente


def agrupar_estaciones_comparacion_directa(campo):
    """
    Algoritmo que compara directamente los patrones de cada estación
    sin usar estructuras nativas intermedias
    """
    estaciones_por_agrupar = ListaEnlazada()

    # Crear lista de todas las estaciones
    actual_estacion = campo.estaciones.cabeza
    while actual_estacion is not None:
        estaciones_por_agrupar.insertar(actual_estacion.dato)
        actual_estacion = actual_estacion.siguiente

    grupos_finales = ListaEnlazada()

    while not estaciones_por_agrupar.esta_vacia():
        # Tomar la primera estación
        estacion_actual = estaciones_por_agrupar.cabeza.dato
        estaciones_por_agrupar.cabeza = estaciones_por_agrupar.cabeza.siguiente
        estaciones_por_agrupar.longitud -= 1

        # Crear nuevo grupo con esta estación
        grupo_actual = ListaEnlazada()
        grupo_actual.insertar(estacion_actual)

        # Buscar estaciones con los mismos patrones
        actual = estaciones_por_agrupar.cabeza
        previo = None

        while actual is not None:
            estacion_comparar = actual.dato

            # Comparar patrones directamente
            patrones_iguales_suelo = patrones_iguales(
                estacion_actual.patron_suelo,
                estacion_comparar.patron_suelo
            )
            patrones_iguales_cultivo = patrones_iguales(
                estacion_actual.patron_cultivo,
                estacion_comparar.patron_cultivo
            )

            if patrones_iguales_suelo and patrones_iguales_cultivo:
                # Agregar al grupo actual
                grupo_actual.insertar(estacion_comparar)

                # Eliminar de la lista por agrupar
                if previo is None:
                    estaciones_por_agrupar.cabeza = actual.siguiente
                else:
                    previo.siguiente = actual.siguiente
                estaciones_por_agrupar.longitud -= 1

                # Continuar con el siguiente
                actual = actual.siguiente
            else:
                previo = actual
                actual = actual.siguiente

        # Convertir el grupo a objeto GrupoEstaciones
        estaciones_grupo = []
        actual_grupo = grupo_actual.cabeza
        while actual_grupo is not None:
            estaciones_grupo.append(actual_grupo.dato)
            actual_grupo = actual_grupo.siguiente

        if estaciones_grupo:
            grupo_obj = GrupoEstaciones(estaciones_grupo)
            grupos_finales.insertar(grupo_obj)

    # Asignar los grupos finales al campo
    campo.grupos_estaciones = grupos_finales


def procesar_campo(campo):
    print(f"➢ Procesando campo {campo.id}")

    # Calcular patrones para cada estación
    calcular_patrones_estaciones(campo)

    # Agrupar estaciones por patrones similares
    agrupar_estaciones_comparacion_directa(campo)

    print(f"➢ Campo {campo.id} procesado exitosamente")
    print(f"➢ Estaciones originales: {campo.estaciones.longitud}")
    print(f"➢ Grupos reducidos: {campo.grupos_estaciones.longitud}")


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
                        ET.SubElement(sensor_xml, 'frecuencia',
                                    idEstacion=grupo.id_representante).text = str(frecuencia_total)

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
                        ET.SubElement(sensor_xml, 'frecuencia',
                                    idEstacion=grupo.id_representante).text = str(frecuencia_total)

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
        print(f"Error al generar archivo de salida: {e}")
        return False