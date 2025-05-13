# algoritmos_geneticos_col/cruce.py

import random

def cruzar(padres, metodo, probabilidad_cruce):
    nueva_poblacion = []
    for i in range(0, len(padres), 2):
        padre1 = padres[i]
        if i + 1 < len(padres):
            padre2 = padres[i + 1]
        else:
            padre2 = random.choice(padres)  # En caso de número impar

        if random.random() < probabilidad_cruce:
            if metodo == 'un_punto':
                hijo1, hijo2 = cruce_un_punto(padre1, padre2)
            elif metodo == 'dos_puntos':
                hijo1, hijo2 = cruce_dos_puntos(padre1, padre2)
            elif metodo == 'uniforme':
                hijo1, hijo2 = cruce_uniforme(padre1, padre2)
            else:
                raise ValueError(f"Método de cruce no reconocido: {metodo}")
        else:
            hijo1, hijo2 = padre1[:], padre2[:]

        nueva_poblacion.append(hijo1)
        nueva_poblacion.append(hijo2)
    return nueva_poblacion

def cruce_un_punto(padre1, padre2):
    punto = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2

def cruce_dos_puntos(padre1, padre2):
    punto1 = random.randint(1, len(padre1) - 2)
    punto2 = random.randint(punto1 + 1, len(padre1) - 1)
    hijo1 = padre1[:punto1] + padre2[punto1:punto2] + padre1[punto2:]
    hijo2 = padre2[:punto1] + padre1[punto1:punto2] + padre2[punto2:]
    return hijo1, hijo2

def cruce_uniforme(padre1, padre2):
    hijo1, hijo2 = [], []
    for gen1, gen2 in zip(padre1, padre2):
        if random.random() < 0.5:
            hijo1.append(gen1)
            hijo2.append(gen2)
        else:
            hijo1.append(gen2)
            hijo2.append(gen1)
    return hijo1, hijo2
