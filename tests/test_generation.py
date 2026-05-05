import unittest
from learning.generation import Generation


# test that population generation and loading functions correctly
class TestCreatePopulation(unittest.TestCase):
    def setUp(self):
        self.gen = Generation()

    def test_gen_player_weights(self):
        base_weights=[[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                      [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]
        
        weights = self.gen.gen_player_weights(base_weights, 2) # TBC

    def test_gen_initial_population(self):
        self.gen.gen_initial_population()
        for i in range(100):
            print(self.gen.population[i])


# test that fitness evaluation functions correctly
class TestEvaluateFitness(unittest.TestCase):
    def setUp(self):
        pass


    def test_(self):
        pass


# test that creation and saving of the following generation functions correctly
class TestNextGeneration(unittest.TestCase):
    def setUp(self):
        pass


    def test_(self):
        pass


if __name__ == "__main__":
    unittest.main()