import unittest
from learning.generation import Generation


# test that population generation, saving and loading functions correctly
class TestGeneration(unittest.TestCase):
    def setUp(self):
        self.gen = Generation()


    def test_gen_player_weights(self):
        base_weights=[[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                      [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]
        weights = self.gen.gen_player_weights(base_weights, 2)
        self.assertEqual(len(weights), len(base_weights))

    
    def test_gen_player_weights_invalid_factor(self):
        base_weights=[[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                      [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]
        self.assertRaises(ValueError, self.gen.gen_player_weights, base_weights, -2)


    def test_gen_initial_population(self):
        self.gen.gen_initial_population(50)
        self.assertEqual(len(self.gen.population), 50)
        self.assertEqual(len(self.gen.population[0]), 4)
        self.assertEqual(len(self.gen.population[0][3]), 4)


    def test_gen_initial_population_large(self):
        self.gen.gen_initial_population(1000)
        self.assertEqual(len(self.gen.population), 1000)
        self.assertEqual(len(self.gen.population[500]), 4)
        self.assertEqual(len(self.gen.population[500][3]), 4)


    def test_load_population(self):
        self.gen.gen_initial_population()
        ex_players = []

        i = 1
        for player in self.gen.population[:3]:
            ex_player = []
            ex_player.append(i)
            ex_player.append(0)
            for weight_group in player[2:]:
                group = []
                for value in weight_group:
                    group.append(value)
                ex_player.append(group)
            ex_players.append(ex_player)
            i += 1
                
        self.gen.save_population_to_file("test_pop.csv", "tests/test_generations/")
        self.gen.load_population_from_file("test_pop.csv", "tests/test_generations/")
        self.assertEqual(self.gen.population[:3], ex_players)
        self.assertEqual(self.gen.generation, 0)


if __name__ == "__main__":
    unittest.main()