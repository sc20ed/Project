from learning.generation import Generation
import logging

log = logging.getLogger("learn.py")

# temporary test method to check initial function
def test_eval():
    gen = Generation()

    # test
    gen.load_population_from_file("test_eval.csv")
    gen.evaluate_fitness()
    
    for row in gen.population:
        print(row)
        print("")