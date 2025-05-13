# algoritmos_geneticos_DG_PV/mutacion.py

import random

def mutar(poblacion, metodo, probabilidad_mutacion):
    nueva_poblacion = []
    for individuo in poblacion:
        if metodo == 'basica':
            nuevo_individuo = mutacion_basica(individuo, probabilidad_mutacion)
        elif metodo == 'aleatoria':
            nuevo_individuo = mutacion_aleatoria(individuo, probabilidad_mutacion)
        else:
            raise ValueError(f"Método de mutación no reconocido: {metodo}")
        nueva_poblacion.append(nuevo_individuo)
    return nueva_poblacion

def mutacion_basica(individuo, probabilidad_mutacion):
    nuevo = []
    for gen in individuo:
        if random.random() < probabilidad_mutacion:
            nuevo.append(1 - gen)  # Cambia 0 a 1 o 1 a 0
        else:
            nuevo.append(gen)
    return nuevo

def mutacion_aleatoria(individuo, probabilidad_mutacion):
    nuevo = []
    for gen in individuo:
        if random.random() < probabilidad_mutacion:
            nuevo.append(random.randint(0,1))  # Reemplaza aleatoriamente
        else:
            nuevo.append(gen)
    return nuevo
