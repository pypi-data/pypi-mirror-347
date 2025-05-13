# algoritmos_geneticos_DG_PV/seleccion.py

import random

def seleccionar(poblacion, aptitudes, metodo):
    if metodo == 'ruleta':
        return seleccion_por_ruleta(poblacion, aptitudes)
    elif metodo == 'torneo':
        return seleccion_por_torneo(poblacion, aptitudes)
    elif metodo == 'aleatorio':
        return seleccion_aleatoria(poblacion)
    else:
        raise ValueError(f"Método de selección no reconocido: {metodo}")

def seleccion_por_ruleta(poblacion, aptitudes):
    suma_aptitud = sum(aptitudes)
    if suma_aptitud == 0:
        # Evitar división por cero
        probabilidades = [1/len(poblacion)] * len(poblacion)
    else:
        probabilidades = [aptitud / suma_aptitud for aptitud in aptitudes]
    
    seleccionados = random.choices(poblacion, weights=probabilidades, k=len(poblacion))
    return seleccionados

def seleccion_por_torneo(poblacion, aptitudes, tamaño_torneo=3):
    seleccionados = []
    for _ in range(len(poblacion)):
        participantes = random.sample(list(zip(poblacion, aptitudes)), tamaño_torneo)
        ganador = max(participantes, key=lambda x: x[1])[0]
        seleccionados.append(ganador)
    return seleccionados

def seleccion_aleatoria(poblacion):
    seleccionados = random.choices(poblacion, k=len(poblacion))
    return seleccionados
