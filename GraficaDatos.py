from graphviz import Digraph
from ClasesPrincipales import CampoAgricola

def graficar_matriz(campo, tipo_matriz,nombre_archivo):
    dot = Digraph(comment=f'Matriz {tipo_matriz} - Campo {campo.id}')

    if tipo_matriz == "frecuencias":
        graficar_matriz_frecuencias(dot, campo)
    elif tipo_matriz == "patrones":
        graficar_matriz_patrones(dot, campo)
    elif tipo_matriz == "reducida":
        graficar_matriz_reducida(dot, campo)

    dot.render(nombre_archivo, format='png', cleanup=True)
    print(f"➢ Gráfica generada: {nombre_archivo}.png")


def graficar_matriz_frecuencias(dot, campo):
    dot.attr('node', shape='box')

    # Crear tabla para sensores de suelo
    with dot.subgraph(name='cluster_suelo') as c:
        c.attr(label='Sensores de Suelo', style='filled', color='lightgrey')
        c.node('suelo_title', 'Sensores Suelo', shape='plaintext')

        # Encabezados de columnas (sensores)
        for j, sensor in enumerate(campo.sensores_suelo):
            c.node(f'sensor_s_{sensor.id}', sensor.id, shape='box')

        # Filas (estaciones) y valores
        for i, estacion in enumerate(campo.estaciones):
            for j, sensor in enumerate(campo.sensores_suelo):
                frecuencia = sensor.obtener_frecuencia(estacion.id)
                if frecuencia > 0:
                    c.node(f'freq_s_{estacion.id}_{sensor.id}', str(frecuencia))
                    c.edge(f'sensor_s_{sensor.id}', f'freq_s_{estacion.id}_{sensor.id}')

    # Crear tabla para sensores de cultivo (similar al anterior)


def graficar_matriz_patrones(dot, campo):
    # Implementación similar a graficar_matriz_frecuencias pero con patrones binarios
    pass


def graficar_matriz_reducida(dot, campo):
    # Implementación para matriz reducida
    pass