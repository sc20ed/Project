from itertools import combinations
#from numpy import random # need to pip install numpy
import logging

log = logging.getLogger("generation.py")


# object to handle generation of player populations through evolutionary learning
class Generation:
    def __init__(self, pop_size, initial_variance=5, mutation_variance=2, pop_to_load=None):
        self.pop_size = pop_size
        self.population = []
        self.initial_variance = initial_variance
        self.mutation_variance = mutation_variance
        self.games_to_eval = 4

        if pop_to_load:
            self.load_population_from_file(pop_to_load)

    
    #
    def generate_initial_population(self):
        pass


    #
    def load_population_from_file(self, filename):
        with open(file=filename, mode='r', encoding="utf-8") as pop:
            pass #load pop by line