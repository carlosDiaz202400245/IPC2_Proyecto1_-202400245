import xml.etree.ElementTree as ET
from EstructuraBase import ListaEnlazada

def cargar_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    campos = ListaEnlazada()

    for campo_xml in root.findall('campo'):
        campo = Campo(campo_xml.get('id'), campo_xml.get('nombre'))
        # Cargar estaciones, sensores y frecuencias
        campos.insertar(campo)
    return campos

def agrupar_estaciones(campo):
    # 1. patrones binarios que nos manden
    # 2. en el segundo paso compararemos filas y agruparemos estaciones
    # 3. sumaremos las frecuanciasss
    pass


def generar_xml_salida(campos, ruta_salida):
    root = ET.Element('camposAgricolas')
    for campo in campos.recorrer():
        campo_xml = ET.SubElement(root, 'campo', id=campo.id, nombre=campo.nombre)
        # Añadir estaciones reducidas, sensores y frecuencias
    ET.ElementTree(root).write(ruta_salida)