# algoritmos_geneticos_DG_PV/reemplazo.py

import random

def reemplazar(poblacion, descendencia, aptitudes, metodo):
    if metodo == 'generacional':
        return reemplazo_generacional(descendencia)
    elif metodo == 'elitismo':
        return reemplazo_elitista(poblacion, descendencia, aptitudes)
    else:
        raise ValueError(f"Método de reemplazo no reconocido: {metodo}")

def reemplazo_generacional(descendencia):
    """
    Reemplaza toda la población anterior por la nueva descendencia.
    """
    return descendencia

def reemplazo_elitista(poblacion, descendencia, aptitudes, porcentaje_elite=0.1):
    """
    Conserva los mejores individuos de la población anterior y completa con descendencia.
    """
    tamaño_elite = max(1, int(len(poblacion) * porcentaje_elite))
    
    # Obtener los mejores individuos
    mejores_indices = sorted(range(len(aptitudes)), key=lambda i: aptitudes[i], reverse=True)[:tamaño_elite]
    elite = [poblacion[i] for i in mejores_indices]

    # Mezclar descendencia
    nueva_poblacion = elite + random.sample(descendencia, len(poblacion) - tamaño_elite)
    return nueva_poblacion
