from itertools import combinations
from random import randint
import logging

log = logging.getLogger("generation.py")


# object to handle generation of player populations through evolutionary learning
class Generation:
    def __init__(self, pop_to_load=None):
        self.generation = 0
        self.pop_size = 0
        self.population = []
        self.crossover_rate = 0.8
        self.mutation_incidence = 0.5
        self.mutation_rate = 0.2
        self.games_to_eval = 4
        self.base_weights = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                             [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]

        if pop_to_load:
            self.load_population_from_file(pop_to_load)

    
    # generate set of heuristic weights
    # each weight is randomly distributed around the base value
    def gen_player_weights(self, base_weights, factor):
        weights = []
        
        # separated grid weights and 
        grid_weights = []
        for value in base_weights[0]:
            diff = int(value * (randint(-100 * factor, 100 * factor)/100))
            grid_weights.append(value + diff)
        weights.append(grid_weights)

        for weight_phase in base_weights[1:]:
            phase = []
            for value in weight_phase:
                diff = value * (randint(-100 * factor, 100 * factor)/100)
                phase.append(round(value + diff, 2))
            weights.append(phase)

        return weights


    # generate population of players from given parameters
    def gen_initial_population(self, size=100, factor=2,
                               base_weights=[[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                                             [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]):
        self.pop_size = size
        
        for i in range(size):
            weights = self.gen_player_weights(base_weights, factor)
            player = [i+1, 0, weights]
            self.population.append(player)


    # load saved population from file
    def load_population_from_file(self, filename):
        with open(file=filename, mode='r', encoding="utf-8") as pop:
            pass #load pop by line


    # run set of evaluation games to determine player fitness
    def run_evaluation_games(self):
        pass


    # evaluate and update fitness of each member of population
    def evaluate_fitness(self):
        pass
    

    # crossover/breed two players to produce two offspring
    def crossover(self):
        pass


    # mutate some weights of population members randomly
    def mutation(self):
        pass


    # generate new population based on the fitness of the previous generation
    def next_generation(self):
        pass


    # save population to file
    def save_generation(self):
        pass

   