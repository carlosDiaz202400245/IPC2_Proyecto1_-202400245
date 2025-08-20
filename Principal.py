from CargarProcesarSalidaDatos import *

def menu():
    while True:
        print("1. Cargar archivo\n2. Procesar archivo\n...")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo: ")
            campos = cargar_xml(ruta)
        elif opcion == "2":
            # procesarArchivo(campos)
            #y lo demas