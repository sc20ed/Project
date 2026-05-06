from learning.generation import Generation
import time
import logging

log = logging.getLogger("learn.py")

# temporary test method to check initial function
def test_eval():
    gen = Generation()

    # test
    gen.gen_initial_population(50)
    time_start = time.time()
    gen.evaluate_fitness()
    time_end = time.time()
    time_elapsed = time_end - time_start
    
    for row in gen.population:
        print(row)
        print("")

    gen.save_population_to_file("testpop50_gen_0.csv")

    log.info("Test 1 completed with time %.3f seconds", time_elapsed)