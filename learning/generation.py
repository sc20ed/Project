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
        self.mutation_scale = 1
        self.guide_weights = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                             [-0.5, 1, 2, 2, 1], [0.5, 1, 2, 1, 1], [1.5, 1, 2, 0.5, 1]]

        if pop_to_load:
            self.load_population_from_file(pop_to_load)


    # copy the weights of a player to avoid reference confusion
    def get_weights(self, player):
        weights = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        
        for i in range(10):
            weights[0][i] = player[3][0][i]

        for i in range(1, 4):
            for j in range(5):
                weights[i][j] = player[3][i][j]

        return weights

    
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
    def save_population_to_file(self, filename, times=["unknown", "unknown", "not reported"],
                                file_dir="learning/saved_generations/"):
        if not self.population:
            return 1
        
        gen_header = ["generation=" + str(self.generation),
                      "start=" + times[0], "end=" + times[1], "time_taken=" + times[2]]
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

            # write each player as row of sequential values
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
                win_loss_draw = []
                for weight in row[2:5]:
                    win_loss_draw.append(int(weight))
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
    def evaluate_fitness(self, population=None):
        if not population:
            population = self.population

        pairs = list(combinations(population, 2))
        with Pool() as pool:
            pair_game_results = pool.starmap(self.run_co_evaluation_games, pairs)
            
        for i, pair in enumerate(pairs):
            for j in range(3):
                pair[0][2][j] += pair_game_results[i][0][j]
                pair[1][2][j] += pair_game_results[i][1][j]

        for player in self.population:
            player[1] = round((player[2][0] + (player[2][2]/2)) / sum(player[2]), 3)
    

    # return a set of weights each selected from parents with equal chance
    def crossover(self, parent_weights):
        weights = []
        grid_weights = []
        for p1, p2 in zip(parent_weights[0][0], parent_weights[1][0]):
            selection = random.randint(0, 1)
            if selection:
                grid_weights.append(p1)
            else:
                grid_weights.append(p2)
        weights.append(grid_weights)

        for p1_w_phase, p2_w_phase in zip(parent_weights[0][1:], parent_weights[1][1:]):
            phase = []
            for p1, p2 in zip(p1_w_phase, p2_w_phase):
                selection = random.randint(0, 1)
                if selection:
                    phase.append(p1)
                else:
                    phase.append(p2)
            weights.append(phase)

        return weights
    

    # create offspring from two parent players
    def breed(self, parent_1, parent_2):
        children = []
        
        # track player index in family for later comparisons
        index_in_family = 1
        parent_weights = [parent_1[3], parent_2[3]]

        # create two children through interpolation
        for i in range(2):
            index_in_family += 1
            child = [index_in_family, 0, [0, 0, 0]]
            child.append(self.gen_player_weights(parent_weights))
            children.append(child)

        # create two children through crossover
        for i in range(2):
            index_in_family += 1
            child = [index_in_family, 0, [0, 0, 0]]
            child.append(self.crossover(parent_weights))

        return children


    # mutate some weights of a player randomly via one of two methods
    def mutate(self, player, method=0):
        mv = self.mutation_scale
        mutated_player = [player[0], player[1], [0, 0, 0]]
        mutated_weights = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        # randomly select elements to mutate significantly
        if method == 0:
            for i in range(10):
                mutation = random.random()
                if mutation < self.mutation_rate:
                    mutated_weights[0][i] = int(player[3][0][i] + 500 * random.uniform(-mv, mv))
                else:
                    mutated_weights[0][i] = int(player[3][0][i])

            for i in range(1, 4):
                for j in range(5):
                    mutation = random.random()
                    if mutation < self.mutation_rate:
                        mutated_weights[i][j] = round(player[3][i][j] + random.uniform(-mv, mv), 2)
                    else:
                        mutated_weights[i][j] = player[3][i][i]
    
        # mutate all elements by a smaller amount
        elif method == 1:
            for i in range(10):
                mutated_weights[0][i] = int(player[3][0][i] + 500 * random.uniform(-mv/4, mv/4))

            for i in range(1, 4):
                for j in range(5):
                    mutated_weights[i][j] += round(player[3][i][j] + random.uniform(-mv/2, mv/2), 2)

        # ensure corner weight is above 500
        if mutated_weights[0][0] < 500:
            mutated_weights[0][0] += 500

        mutated_player.append(mutated_weights)
        return mutated_player
    

    # evaluate fitness within family of players and return the best four
    def family_co_evaluation(self, family):
        pairs = list(combinations(family, 2))
        for pair in pairs:
            pair_game_result = self.run_co_evaluation_games(pair[0], pair[1])
            for i in range(3):
                family[pair[0][0]][2][i] += pair_game_result[0][i]
                family[pair[1][0]][2][i] += pair_game_result[1][i]

        for player in family:
            player[1] = round((player[2][0] + (player[2][2]/2)) / sum(player[2]), 3)
        trimmed_family = sorted(family, key=lambda wld: wld[1], reverse=True)[:4]

        return trimmed_family
    

    # generate new population based on the fitness of the previous generation
    def next_generation(self):
        new_pop = []
        pop_count = 0

        # keep the top 10% of the population so good players don't disappear
        pop = sorted(self.population, key=lambda player: player[1], reverse=True)
        elt_cut = int(len(pop)*0.1)
        elitism_selection = pop[:elt_cut]
        for player in elitism_selection:
            pop_count += 1
            new_pop.append([pop_count, 0, [0, 0, 0], self.get_weights(player)])

        # select 50% (minus the elitism selection) of the population for parents by fitness
        # fitness^4 is used for weighting so that higher fitness players are selected more frequently
        # the * 10 in (choice[1]*10)**4 is for testing readability
        # this may also ensure floating point precision issues are avoided
        prob_selection = []
        fitness_weights = []     
        for player in pop:
            fitness_weights.append((player[1]*10)**4)
        for i in range(int((len(pop) - elt_cut)/2)): 
            choice = random.choices(pop, fitness_weights, k=1)[0]
            pop.remove(choice)
            fitness_weights.remove((choice[1]*10)**4)
            choice[1] = 0
            choice[2] = [0, 0, 0]
            prob_selection.append(choice)
        random.shuffle(prob_selection)

        # crossover parents to produce four children, then mutate
        families = []
        while len(prob_selection) > 1:
            parent_1 = prob_selection.pop()
            parent_2 = prob_selection.pop()
            parent_1[0], parent_2[0] = 0, 1
            children = self.breed(parent_1, parent_2)
            family = [parent_1, parent_2]
            family.extend(children)

            # mutate members of the family with preset chance
            mutated_family = []
            for player in family:
                mutation = random.random()
                if mutation < self.mutation_incidence:
                    mutated_player = self.mutate(player)
                    mutated_family.append(mutated_player)
                else:
                    mutated_family.append(player)
            families.append(mutated_family)

        # if fitness selection is odd, insert remaining player clean and mutated
        if prob_selection:
            pop_count += 1
            mutated_player = self.mutate(prob_selection[0], 0)
            new_pop.append([pop_count, 0, [0, 0, 0], self.get_weights(mutated_player)])
            mutated_player = self.mutate(prob_selection.pop(), 1)
            pop_count += 1
            new_pop.append([pop_count, 0, [0, 0, 0], self.get_weights(mutated_player)])

        # execute family evaluation and trimming in parallel
        with Pool() as pool:
            trimmed_families = pool.map(self.family_co_evaluation, families)

        for family in trimmed_families:
            for player in family:
                pop_count += 1
                new_pop.append([pop_count, 0, [0, 0, 0], self.get_weights(player)])
    
        self.population = new_pop
        self.generation += 1
        
        for row in new_pop:
            print("")
            print(row)
