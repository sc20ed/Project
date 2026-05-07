from learning.generation import Generation
import time
import logging

log = logging.getLogger("learn.py")

# temporary test method to check initial function
def test_eval():
    gen = Generation()

    # test
    time_start = time.time()
    gen.gen_initial_population(5)
    gen.evaluate_fitness()

    for row in gen.population:
        print(row)
        print("")

    new_pop = gen.next_generation()

    print("POP")

    for row in new_pop:
        print(row)
        print("")

    print(len(new_pop))

    time_end = time.time()
    time_elapsed = time_end - time_start

    log.info("Test 1 completed with time %3.3f seconds", time_elapsed)