from graphviz import Digraph

def graficar_matriz(campo, tipo_matriz):
    dot = Digraph()
    # Añadir nodos de estaciones, sensores y aristas osea frecuencias pe
    dot.render(f'matriz_{tipo_matriz}', format='png')