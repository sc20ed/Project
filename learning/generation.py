from othello.game import run_game
from itertools import combinations
from multiprocessing import Pool
import random
import csv
import logging

log = logging.getLogger("generation.py")


# object to handle generation of player populations through evolutionary learning
class Generation:
    def __init__(self, pop_to_load=None, board_size=8, depth=2, n_game_sets=2):
        self.generation = 0
        self.population = []
        self.board_size = board_size
        self.depth = depth
        self.n_game_sets = n_game_sets
        self.crossover_rate = 0.8
        self.mutation_incidence = 0.5
        self.mutation_rate = 0.2
        self.guide_weights = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                             [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]

        if pop_to_load:
            self.load_population_from_file(pop_to_load)

    
    # generate set of heuristic weights
    # each weight is randomly distributed around the base value
    def gen_player_weights(self, base_weights):
        weights = []
        
        # separated grid weights and weight phases as grid weights should be separately tunable
        # additionally, the corner is not allowed below 500, as this is intuitively bad
        grid_weights = []
        for floor, ceiling in zip(base_weights[0][0], base_weights[1][0]):
            if floor >= ceiling:
                floor, ceiling = ceiling, floor
            value = random.randint(floor, ceiling)
            grid_weights.append(value)
        weights.append(grid_weights)

        for f_w_phase, c_w_phase in zip(base_weights[0][1:], base_weights[1][1:]):
            phase = []
            for floor, ceiling in zip(f_w_phase, c_w_phase):
                if floor >= ceiling:
                    floor, ceiling = ceiling, floor
                value = round(random.uniform(floor, ceiling), 2)
                phase.append(value)
            weights.append(phase)

        return weights


    # generate population of players from given parameters
    def gen_initial_population(self, size=10,
                               base_weight_floor=[[500, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000],
                                                  [-3, -3, -3,-3,-3], [-3, -3,-3,-3,-3], [-3, -3, -3, -3, -3]],
                               base_weight_ceiling=[[5000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
                                                    [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]],):
        self.generation = 0
        self.population.clear()
        base_weights = [base_weight_floor, base_weight_ceiling]

        for i in range(size):
            weights = self.gen_player_weights(base_weights)
            player = [i+1, 0, [0, 0, 0], weights]
            self.population.append(player)

    
    # save population to file
    def save_population_to_file(self, filename, file_dir="learning/saved_generations/"):
        if not self.population:
            return 1
        
        gen_header = ["generation=" + str(self.generation)]
        p_header = ["player", "fitness", "win", "loss", "draw",
                  "gw1", "gw2", "gw3", "gw4", "gw5", "gw6", "gw7", "gw8", "gw9", "gw10", 
                  "gp1_w1", "gp1_w2", "gp1_w3", "gp1_w4", "gp1_w5",
                  "gp2_w1", "gp2_w2", "gp2_w3", "gp2_w4", "gp2_w5",
                  "gp3_w1", "gp3_w2", "gp3_w3", "gp3_w4", "gp3_w5"]
        
        file_path= file_dir + filename
        with open(file_path, mode='w', newline='') as file:
            players = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
            players.writerow(gen_header)
            players.writerow(p_header)

            # write each player as row of sequential values in file
            for player in self.population:
                row = [player[0], player[1]]
                for score in player[2]:
                    row.append(score)
                for weights in player[3:]:
                    for weight_group in weights:
                        for value in weight_group:
                            row.append(value)

                players.writerow(row)


    # load saved population from file
    def load_population_from_file(self, filename, file_dir="learning/saved_generations/"):
        self.population.clear()

        file_path = file_dir + filename
        with open(file_path, mode='r', newline='') as file:
            players = csv.reader(file, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
            self.generation = int(next(players, None)[0][-1])
            next(players, None)
            
            for row in players:
                win_loss_draw = row[2:5]
                grid_weights = []
                for weight in row[5:15]:
                    grid_weights.append(int(weight))
                weight_phase_1 = row[15:20]
                weight_phase_2 = row[20:25]
                weight_phase_3 = row[25:]
                weights = []
                weights.append(grid_weights)
                weights.append(weight_phase_1)
                weights.append(weight_phase_2)
                weights.append(weight_phase_3)

                player = [int(row[0]), int(row[1]), win_loss_draw, weights]
                self.population.append(player)


    # run set of evaluation games for pair of players and update win-loss-draw
    def run_co_evaluation_games(self, p1, p2):
        p1_wins = 0
        p2_wins = 0
        draws = 0

        # run half of the games black and half white for each player
        # track wins from original player order
        for i in range(self.n_game_sets):
            g1_win = run_game(self.board_size, 2, self.depth, p1[3], 2, self.depth, p2[3], 4)[0]
            if g1_win == 1:
                p1_wins += 1
            elif g1_win == -1:
                p2_wins += 1
            else:
                draws += 1

            g2_win = run_game(self.board_size, 2, self.depth, p2[3], 2, self.depth, p1[3], 4)[0] * -1
            if g2_win == 1:
                p1_wins += 1
            elif g2_win == -1:
                p2_wins += 1
            else:
                draws += 1

        p1_wld = [p1_wins, p2_wins, draws]
        p2_wld = [p2_wins, p1_wins, draws]
        return p1_wld, p2_wld


    # run evaluation games in parallel and update fitness of each member of population
    def evaluate_fitness(self):
        pairs = list(combinations(self.population, 2))
        with Pool() as pool:
            pair_game_results = pool.starmap(self.run_co_evaluation_games, pairs)
            
        for i, pair in enumerate(pairs):
            for j in range(3):
                pair[0][2][j] += pair_game_results[i][0][j]
                pair[1][2][j] += pair_game_results[i][1][j]

        for player in self.population:
            player[1] = round((player[2][0] + (player[2][2]/2)) / sum(player[2]), 3)
    

    # crossover/breed two players to produce two offspring
    def crossover(self, parent_1, parent_2):
        
        # create two children
        # one is random distance inbetween, and one randomly selects a value from both parents

        parents = [parent_1, parent_2]
        child_1 = self.gen_player_weights(parents)
        child_2 = self.gen_player_weights(parents)

        return child_1, child_2


    # mutate some weights of population members randomly
    def mutation(self):
        pass
        # mutate genes by small factor
        # or mutate x% of genes somewhat


    # generate new population based on the fitness of the previous generation
    def next_generation(self):
        new_pop = []
        pop = sorted(self.population, key=lambda player: player[1], reverse=True)
        elitist_selection = pop[:int(len(pop)*0.1)]
        for i, player in enumerate(elitist_selection):
            new_pop.append([i+1, 0, [0, 0, 0], player[3]])
                           
        for i in range(int(len(pop)*0.1)):
            pop.pop()

        mutation_count = 0
        random.shuffle(pop)
        while len(pop) > 1:
            parent_1 = pop.pop()[3]
            parent_2 = pop.pop()[3]
            child_1, child_2 = self.crossover(parent_1, parent_2)
            family = [parent_1, parent_2, child_1, child_2]
            rand_s1 = random.randint(0, 3)
            rand_s2 = random.randint(0, 3)
            survivor_1, survivor_2 = [family[rand_s1], family[rand_s2]] #family_tournament(family)
            if random.random() > self.mutation_incidence:
                mutation_count += 1
            # fix to player format TBC
            new_pop.append([new_pop[-1][0] + 1, 0, [0, 0, 0], survivor_1])
            new_pop.append([new_pop[-1][0] + 1, 0, [0, 0, 0], survivor_2])
        
        if pop:
            new_pop.append([new_pop[-1][0] + 1, 0, [0, 0, 0], pop.pop()[3]])

        print(mutation_count)

        return new_pop

        # take current pop
        # save top 10%
        # replace bottom 10% with initial gens
        # for the remaining 90%, randomly pair up and crossbreed
        # for the children, mutate one child a little and one a lot 
        # play a 4 game check tournament and add the two fittest to the new population
        # pop = top 10% + bred and mutated + regen 10%
        # gen += 1
