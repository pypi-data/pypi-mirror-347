# algoritmos_geneticos_DG_PV/genetico.py

import random
from algoritmos_geneticos_DG_PV import seleccion, cruce, mutacion, reemplazo

class AlgoritmoGenetico:
    def __init__(self,
                 tamaño_poblacion,
                 num_generaciones,
                 funcion_fitness,
                 metodo_seleccion='torneo',
                 metodo_cruce='un_punto',
                 metodo_mutacion='basica',
                 metodo_reemplazo='generacional',
                 probabilidad_cruce=0.8,
                 probabilidad_mutacion=0.1):
        """
        Inicializa el algoritmo genético.

        Parámetros:
        - tamaño_poblacion (int): número de individuos.
        - num_generaciones (int): número de generaciones.
        - funcion_fitness (function): función para evaluar aptitud.
        - metodo_seleccion (str): método de selección.
        - metodo_cruce (str): método de cruce.
        - metodo_mutacion (str): método de mutación.
        - metodo_reemplazo (str): método de reemplazo.
        - probabilidad_cruce (float): probabilidad de cruce.
        - probabilidad_mutacion (float): probabilidad de mutación.
        """
        self.tamaño_poblacion = tamaño_poblacion
        self.num_generaciones = num_generaciones
        self.funcion_fitness = funcion_fitness
        self.metodo_seleccion = metodo_seleccion
        self.metodo_cruce = metodo_cruce
        self.metodo_mutacion = metodo_mutacion
        self.metodo_reemplazo = metodo_reemplazo
        self.probabilidad_cruce = probabilidad_cruce
        self.probabilidad_mutacion = probabilidad_mutacion
        self.poblacion = []
    
    def inicializar_poblacion(self, tamaño_genoma):
        """
        Crea la población inicial con genomas aleatorios de 0s y 1s.
        """
        self.poblacion = [[random.randint(0,1) for _ in range(tamaño_genoma)] for _ in range(self.tamaño_poblacion)]

    def evolucionar(self):
        """
        Ejecuta el ciclo completo de generaciones.
        """
        for generacion in range(self.num_generaciones):
            # Evaluar aptitud
            aptitudes = [self.funcion_fitness(individuo) for individuo in self.poblacion]

            # Seleccionar padres
            padres = seleccion.seleccionar(self.poblacion, aptitudes, self.metodo_seleccion)

            # Cruzar padres
            descendencia = cruce.cruzar(padres, self.metodo_cruce, self.probabilidad_cruce)

            # Mutar descendencia
            descendencia = mutacion.mutar(descendencia, self.metodo_mutacion, self.probabilidad_mutacion)

            # Reemplazar población
            self.poblacion = reemplazo.reemplazar(self.poblacion, descendencia, aptitudes, self.metodo_reemplazo)

            print(f"Generación {generacion+1} completada.")

    def obtener_mejor_individuo(self):
        """
        Retorna el mejor individuo de la población actual.
        """
        aptitudes = [self.funcion_fitness(individuo) for individuo in self.poblacion]
        indice_mejor = aptitudes.index(max(aptitudes))
        return self.poblacion[indice_mejor], aptitudes[indice_mejor]
