# tests/test_genetico.py

import unittest
from algoritmos_geneticos_DG_PV.genetico import AlgoritmoGenetico

class TestAlgoritmoGenetico(unittest.TestCase):
    def setUp(self):
        # Definir una función de aptitud simple
        self.funcion_fitness = lambda individuo: sum(individuo)

        # Crear instancia del algoritmo
        self.algoritmo = AlgoritmoGenetico(
            tamaño_poblacion=10,
            num_generaciones=5,
            funcion_fitness=self.funcion_fitness,
            metodo_seleccion='torneo',
            metodo_cruce='un_punto',
            metodo_mutacion='basica',
            metodo_reemplazo='elitismo',
            probabilidad_cruce=0.9,
            probabilidad_mutacion=0.05
        )

        self.algoritmo.inicializar_poblacion(tamaño_genoma=8)

    def test_inicializacion_poblacion(self):
        self.assertEqual(len(self.algoritmo.poblacion), 10)
        self.assertEqual(len(self.algoritmo.poblacion[0]), 8)

    def test_evolucionar(self):
        self.algoritmo.evolucionar()
        mejor, aptitud = self.algoritmo.obtener_mejor_individuo()
        self.assertIsInstance(mejor, list)
        self.assertIsInstance(aptitud, int)

if __name__ == "__main__":
    unittest.main()