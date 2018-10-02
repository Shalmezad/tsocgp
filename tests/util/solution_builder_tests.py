from tsocgp.gp import Genome
from tsocgp.util import Annotator
from tsocgp.util import SolutionBuilder
import tsocgp.validation as validation
import unittest
import json
import os

class SolutionBuilderTests(unittest.TestCase):
    def test_solution_from_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            annotated_problem = Annotator.annotate(problem)
            genome = Genome()
            genome.genesis(annotated_problem)
            solution = SolutionBuilder.build_solution(annotated_problem, genome)
            #print(solution)
            # SHOULD PASS ALL VALIDATIONS
            # Each train scheduled:
            validator = validation.EachTrainIsScheduledValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}\n{}".format(results, solution))
            # Has problem instance hash:
            validator = validation.ProblemInstanceHashPresentValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}\n{}".format(results, solution))
            # Meets earliest requirements:
            validator = validation.TimeWindowsForEarliestRequirementsValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}\n{}".format(results, solution))
            # Meets section requirements:
            validator = validation.PassThroughAllSectionRequirementsValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}\n{}".format(results, solution))