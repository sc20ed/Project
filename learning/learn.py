from learning.generation import Generation
import time
import logging

log = logging.getLogger("learn.py")

# temporary test method to check initial function
def test_eval():
    gen = Generation()

    # test
    time_start = time.time()
    gen.gen_initial_population(10)
    gen.evaluate_fitness()
    gen.save_population_to_file("test3_gen0.csv")
    gen.next_generation()
    time_end = time.time()

    time_elapsed = str(round(time_end - time_start, 3)) + " seconds"
    gen.save_population_to_file("test3_gen1.csv", time_elapsed)
    log.info("Test 1 completed with time %s", time_elapsed)