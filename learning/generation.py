from random import randint
import csv
from itertools import combinations
import logging

log = logging.getLogger("generation.py")


# object to handle generation of player populations through evolutionary learning
class Generation:
    def __init__(self, pop_to_load=None):
        self.generation = 0
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
        
        # separated grid weights and weight phases as grid weights should be less variable
        grid_weights = []
        wg_factor = int(factor/2)
        for value in base_weights[0]:
            diff = int(value * (randint(-100 * wg_factor, 100 * wg_factor)/100))
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
        self.generation = 0
        for i in range(size):
            weights = self.gen_player_weights(base_weights, factor)
            player = [i+1, 0, weights]
            self.population.append(player)


    # load saved population from file
    def load_population_from_file(self, filename, file_dir="learning/saved_generations/"):
        self.population.clear()

        file_path = file_dir + filename
        with open(file_path, mode='r', newline='') as file:
            players = csv.reader(file, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
            self.generation = int(next(players, None)[0][-1])
            next(players, None)
            
            for row in players:
                grid_weights = []
                for weight in row[2:12]:
                    grid_weights.append(int(weight))

                weight_phase_1 = row[12:17]
                weight_phase_2 = row[17:22]
                weight_phase_3 = row[22:]

                weights = []
                weights.append(grid_weights)
                weights.append(weight_phase_1)
                weights.append(weight_phase_2)
                weights.append(weight_phase_3)

                player = [int(row[0]), int(row[1]), weights]
                self.population.append(player)


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
    def save_population_to_file(self, filename, file_dir="learning/saved_generations/"):
        if not self.population:
            return 1
        
        gen_header = ["generation=" + str(self.generation)]
        p_header = ['player', 'fitness',
                  'gw1', 'gw2', 'gw3', 'gw4', 'gw5', 'gw6', 'gw7', 'gw8', 'gw9', 'gw10', 
                  'gp1_w1', 'gp1_w2', 'gp1_w3', 'gp1_w4', 'gp1_w5',
                  'gp2_w1', 'gp2_w2', 'gp2_w3', 'gp2_w4', 'gp2_w5',
                  'gp3_w1', 'gp3_w2', 'gp3_w3', 'gp3_w4', 'gp3_w5']
        
        file_path= file_dir + filename
        with open(file_path, mode='w', newline='') as file:
            players = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
            players.writerow(gen_header)
            players.writerow(p_header)

            for player in self.population:
                row = [player[0], player[1]]
                for weights in player[2:]:
                    for weight_group in weights:
                        for value in weight_group:
                            row.append(value)

                players.writerow(row)
                
            
   