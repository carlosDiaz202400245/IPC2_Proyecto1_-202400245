from CargarProcesarSalidaDatos import procesar_campo, generar_xml_salida
from GraficaDatos import GraficadoraDatos
from ClasesPrincipales import CampoAgricola, Estacion, SensorSuelo, SensorCultivo, Frecuencia
from EstructuraBase import ListaEnlazada
import xml.etree.ElementTree as ET

# Variables globales
campos_cargados = ListaEnlazada()
graficadora = GraficadoraDatos()


def cargar_xml(ruta_archivo):
    """Función para cargar archivo XML"""
    global campos_cargados
    try:
        print(f"➢ Cargando archivo: {ruta_archivo}")

        # Parsear el XML
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()

        # Limpiar datos anteriores
        campos_cargados = ListaEnlazada()

        # Procesar cada campo agrícola
        for campo_elem in root.findall('campo'):
            campo_id = campo_elem.get('id')
            campo_nombre = campo_elem.get('nombre')
            campo = CampoAgricola(campo_id, campo_nombre)

            print(f"➢ Cargando campo agrícola {campo_id}")

            # Procesar estaciones base
            estaciones_base = campo_elem.find('estacionesBase')
            if estaciones_base is not None:
                for estacion_elem in estaciones_base.findall('estacion'):
                    estacion_id = estacion_elem.get('id')
                    estacion_nombre = estacion_elem.get('nombre')
                    estacion = Estacion(estacion_id, estacion_nombre)
                    campo.agregar_estacion(estacion)
                    print(f"➢ Creando estación base {estacion_id}")

            # Procesar sensores de suelo
            sensores_suelo = campo_elem.find('sensoresSuelo')
            if sensores_suelo is not None:
                for sensor_elem in sensores_suelo.findall('sensor'):
                    sensor_id = sensor_elem.get('id')
                    sensor_nombre = sensor_elem.get('nombre')
                    sensor = SensorSuelo(sensor_id, sensor_nombre)

                    # Procesar frecuencias
                    for freq_elem in sensor_elem.findall('frecuencia'):
                        id_estacion = freq_elem.get('idEstacion')
                        valor = int(freq_elem.text.strip())
                        sensor.agregar_frecuencia(id_estacion, valor)

                    campo.agregar_sensor_suelo(sensor)

            # Procesar sensores de cultivo
            sensores_cultivo = campo_elem.find('sensoresCultivo')
            if sensores_cultivo is not None:
                for sensor_elem in sensores_cultivo.findall('sensorT'):
                    sensor_id = sensor_elem.get('id')
                    sensor_nombre = sensor_elem.get('nombre')
                    sensor = SensorCultivo(sensor_id, sensor_nombre)

                    # Procesar frecuencias
                    for freq_elem in sensor_elem.findall('frecuencia'):
                        id_estacion = freq_elem.get('idEstacion')
                        valor = int(freq_elem.text.strip())
                        sensor.agregar_frecuencia(id_estacion, valor)

                    campo.agregar_sensor_cultivo(sensor)

            # Agregar campo a la lista
            campos_cargados.insertar(campo)

        print("✅ Archivo cargado exitosamente")
        return campos_cargados

    except Exception as e:
        print(f"❌ Error al cargar archivo: {e}")
        return None


def _lista_esta_vacia(lista_enlazada):
    """Verifica si una lista enlazada está vacía"""
    return lista_enlazada.cabeza is None


def procesar_archivo():
    """Función para procesar el archivo cargado"""
    global campos_cargados
    if _lista_esta_vacia(campos_cargados):
        print("❌ Error: Primero debe cargar un archivo (Opción 1)")
        return

    print("➢ Procesando archivo...")

    actual_campo = campos_cargados.cabeza
    while actual_campo is not None:
        campo = actual_campo.dato
        print(f"➢ Procesando campo {campo.id}: {campo.nombre}")

        # Procesar cada estación
        actual_estacion = campo.estaciones.cabeza
        while actual_estacion is not None:
            estacion = actual_estacion.dato
            print(f"➢ Procesando estación base {estacion.id}")
            actual_estacion = actual_estacion.siguiente

        # Procesar el campo
        procesar_campo(campo)
        actual_campo = actual_campo.siguiente

    print("✅ Archivo procesado exitosamente")


def escribir_archivo_salida():
    """Función para escribir archivo de salida"""
    global campos_cargados
    if _lista_esta_vacia(campos_cargados):
        print("❌ Error: No hay datos procesados para generar salida")
        return

    print("Opción generar archivo de salida")
    ruta = input("Ingrese la ruta del archivo: ").strip()
    nombre = input("Ingrese el nombre del archivo: ").strip()

    archivo_salida = f"{ruta}/{nombre}" if ruta else nombre
    success = generar_xml_salida(campos_cargados, archivo_salida)

    if success:
        print("✅ Archivo de salida generado exitosamente")
    else:
        print("❌ Error al generar archivo de salida")


def mostrar_datos_estudiante():
    """Muestra los datos del estudiante"""
    print("\n" + "=" * 50)
    print("DATOS DEL ESTUDIANTE")
    print("=" * 50)
    print("➢ Nombre del estudiante: [Tu Nombre Completo]")
    print("➢ Carnet del estudiante: [Tu Carnet]")
    print("➢ Curso: Introducción a la Programación y Computación 2")
    print("➢ Sección: [Tu Sección]")
    print("➢ Carrera: Ingeniería en Ciencias y Sistemas")
    print("➢ Semestre: 4to Semestre")
    print("➢ Enlace a documentación: [Tu URL de GitHub]")
    print("=" * 50)


def generar_grafica():
    """Función para generar gráficas"""
    global campos_cargados, graficadora

    if _lista_esta_vacia(campos_cargados):
        print("❌ Error: Primero debe cargar un archivo (Opción 1)")
        return

    print("\n--- GENERAR GRÁFICA ---")

    # Mostrar campos disponibles
    print("Campos agrícolas disponibles:")
    contador = 1
    campos_lista = []
    actual_campo = campos_cargados.cabeza
    while actual_campo is not None:
        campo = actual_campo.dato
        print(f"{contador}. {campo.nombre} (ID: {campo.id})")
        campos_lista.append(campo)
        contador += 1
        actual_campo = actual_campo.siguiente

    try:
        seleccion = int(input("Seleccione el número del campo: ")) - 1
        if seleccion < 0 or seleccion >= len(campos_lista):
            print("❌ Selección inválida")
            return

        campo_seleccionado = campos_lista[seleccion]

        print("\nTipo de gráfica:")
        print("1. Matriz de Frecuencias")
        print("2. Matriz de Patrones")
        print("3. Matriz Reducida")

        tipo_opcion = input("Seleccione el tipo de gráfica (1-3): ").strip()

        if tipo_opcion == "1":
            tipo_grafica = "frecuencias"
        elif tipo_opcion == "2":
            tipo_grafica = "patrones"
        elif tipo_opcion == "3":
            tipo_grafica = "reducida"
        else:
            print("❌ Opción inválida")
            return

        nombre_archivo = input("Ingrese el nombre para el archivo de la gráfica: ").strip()
        if not nombre_archivo:
            nombre_archivo = f"grafica_{campo_seleccionado.id}_{tipo_grafica}"

        # Generar la gráfica
        success = graficadora.generar_grafica(campo_seleccionado, tipo_grafica, nombre_archivo)
        if success:
            print("✅ Gráfica generada exitosamente")
            print(f"➢ La gráfica se ha guardado como: {nombre_archivo}.png")

    except ValueError:
        print("❌ Entrada inválida. Debe ingresar un número.")
    except Exception as e:
        print(f"❌ Error al generar gráfica: {e}")


def menu():
    """Menú principal del programa"""
    global campos_cargados

    while True:
        print("\n" + "=" * 50)
        print("MENÚ PRINCIPAL - SISTEMA AGRICULTURA DE PRECISIÓN")
        print("=" * 50)
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salir")
        print("=" * 50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("Opción cargar archivo")
            ruta = input("Ingrese la ruta del archivo: ").strip()
            nombre = input("Ingrese el nombre del archivo: ").strip()
            archivo_completo = f"{ruta}/{nombre}" if ruta else nombre
            campos_cargados = cargar_xml(archivo_completo)

        elif opcion == "2":
            procesar_archivo()

        elif opcion == "3":
            escribir_archivo_salida()

        elif opcion == "4":
            mostrar_datos_estudiante()

        elif opcion == "5":
            generar_grafica()

        elif opcion == "6":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu()