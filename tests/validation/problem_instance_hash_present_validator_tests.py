from tsocgp.validation import ProblemInstanceHashPresentValidator
import unittest
import json

class ProblemInstanceHashPresentValidatorTests(unittest.TestCase):
    def test_good_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            solution = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            with open('data/sample_scenario_solution.json') as f:
                solution = json.load(f)
            validator = ProblemInstanceHashPresentValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}".format(results))


    def test_missing_key(self):
        problem = {}
        problem['hash'] = 72
        solution = {}
        validator = ProblemInstanceHashPresentValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(1, len(results))


    def test_wrong_key(self):
        problem = {}
        problem['hash'] = 72
        solution = {}
        solution['problem_instance_hash'] = 42
        validator = ProblemInstanceHashPresentValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(1, len(results))

    def test_right_key(self):
        problem = {}
        problem['hash'] = 72
        solution = {}
        solution['problem_instance_hash'] = 72
        validator = ProblemInstanceHashPresentValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(0, len(results))