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
    current_datetime = str(datetime.datetime.now())
    gen.save_population_to_file(file, [current_datetime, str(datetime.datetime.now()), "n/a"])
    log.info("Saved population of size %d to %s", size, filename)


# evolve population of players for a given number of generations and save each generation to new file
def evolve(filename="temp", generations=1, board_size=8):
    file = filename + ".csv"
    gen = Generation()
    gen.load_population_from_file(file)

    file_n = filename + "_gen_" + str(gen.generation) + ".csv"
    datetime_start_old = str(datetime.datetime.now())
    time_start_old = time.time()
    gen.save_population_to_file(file_n, [datetime_start_old, str(datetime.datetime.now()), "n/a"])
    
    # main evolution loop
    # calculates datetimes and time elapsed for a generation initially as when
    # the next_generation() function was called, then updates once fitness evaluation is complete
    for i in range(generations):
        print("Running evolution of " + file_n + " generation " + str(gen.generation) + "...")
        gen.load_population_from_file(file_n)

        gen.evaluate_fitness()
        time_elapsed = str(round(time.time() - time_start_old, 3)) + " seconds"
        gen.save_population_to_file(file_n, [datetime_start_old, str(datetime.datetime.now()), time_elapsed])
        log.info("Evaluated fitness of %s", file_n)
        
        datetime_start = str(datetime.datetime.now())
        time_start = time.time()
        gen.next_generation()
        log.info("Produced generation %d from %s", gen.generation, file_n)
        time_elapsed = str(round(time.time() - time_start, 3)) + " seconds"

        file_n = filename + "_gen_" + str(gen.generation) + ".csv"
        gen.save_population_to_file(file_n, [datetime_start, str(datetime.datetime.now()), time_elapsed])
        log.info("Saved generation %d to %s", gen.generation, file_n)
        datetime_start_old = datetime_start
        time_start_old = time_start
    
    # evaluate the final generation
    gen.load_population_from_file(file_n)
    gen.evaluate_fitness()
    time_elapsed = str(round(time.time() - time_start_old, 3)) + " seconds"
    gen.save_population_to_file(file_n, [datetime_start_old, str(datetime.datetime.now()), time_elapsed])
    log.info("Evaluated fitness of %s", file_n)

    


# evaluate population fitness separately
def standalone_fitness_evaluation(filename="temp", board_size=8):
    file = filename + ".csv"
    gen = Generation()
    gen.load_population_from_file(file)
    gen.evaluate_fitness()
    gen.save_population_to_file(file)
    log.info("Evaluated fitness of %s", filename)