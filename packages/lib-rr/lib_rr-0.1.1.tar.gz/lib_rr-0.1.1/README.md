# lib_rr

Esta es una librería de ejemplo que incluye algoritmos genéticos y funciones matemáticas útiles.

## Instalación

Puedes instalar la librería utilizando pip:

pip install lib_rr


## Uso

### Funciones disponibles

#### `crear_individuo(valor_min, valor_max)`
Genera un número aleatorio entre un valor mínimo y máximo.

```python
from lib_rr import Funciones

individuo = Funciones.crear_individuo(0, 10)
print(individuo)

ejecutar_algoritmo_genetico(tam_poblacion, ngen, p_cruce, p_mutacion, B, latitud, invierno)
Ejecuta un algoritmo genético para optimizar la distancia mínima entre paneles solares.

from lib_rr import algoritmo_genetico

mejor_beta, mejor_DM, mejores = algoritmo_genetico.ejecutar_algoritmo_genetico(
    tam_poblacion=100, ngen=50, p_cruce=0.7, p_mutacion=0.1, B=10, latitud=4, invierno=True
)
print(mejor_beta, mejor_DM)
