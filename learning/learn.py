from learning.generation import Generation
import datetime
import time
import logging

log = logging.getLogger("learn.py")


# generate initial population and save to file
def generate_players(filename="temp", size=100):
    file = filename + ".csv"
    gen = Generation()
    gen.gen_initial_population(size)
    gen.save_population_to_file(file)
    log.info("Saved population of size %d to %s", size, filename)


# evolve population of players for a given number of generations and save each generation to new file
def evolve(filename="temp", generations=1, board_size=8):
    file = filename + ".csv"
    gen = Generation()
    gen.load_population_from_file(file)

    file_n = filename + "_gen_" + str(gen.generation) + ".csv"
    gen.save_population_to_file(file_n)

    for i in range(generations):
        print("Running evolution of " + file_n + " generation " + str(gen.generation) + "...")
        gen.load_population_from_file(file_n)
        datetime_start = str(datetime.datetime.now())
        time_start = time.time()
        gen.evaluate_fitness()
        log.info("Evaluated fitness of %s", file_n)
        gen.next_generation()
        log.info("Produced generation %d from %s", gen.generation, file_n)
        time_end = time.time()
        datetime_end = str(datetime.datetime.now())
        time_elapsed = str(round(time_end - time_start, 3)) + " seconds"
        file_n = filename + "_gen_" + str(gen.generation) + ".csv"
        gen.save_population_to_file(file_n, [datetime_start, datetime_end, time_elapsed])
        log.info("Saved generation %d to %s", gen.generation, file_n)


# evaluate population fitness separately
def standalone_fitness_evaluation(filename="temp", board_size=8):
    file = filename + ".csv"
    gen = Generation()
    gen.load_population_from_file(file)
    gen.evaluate_fitness()
    gen.save_population_to_file(file)
    log.info("Evaluated fitness of %s", filename)