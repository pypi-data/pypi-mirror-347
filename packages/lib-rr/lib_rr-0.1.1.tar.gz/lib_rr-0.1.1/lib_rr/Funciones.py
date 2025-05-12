#Funciones.py
import random   # Importar random para generar numeros aleatorios

# Funcion objetivo a minimizar
def funcion_objetivo(x):
    # """ calcula el cuadrado del valor de x. """
    return x ** 2

# Crear un individuo aleatorio
def crear_individuo(valor_min, valor_max):
    # """ Genera un numero aleatorio dentro de un rango especifico """
    return random.uniform(valor_min, valor_max)
print (crear_individuo)         

# crear una poblacion inicial
def crear_poblacion(tamano, valor_min, valor_max):
    # Genera una lista de individuos aleatorios
    return [crear_individuo(valor_min, valor_max) for _ in range(tamano)]