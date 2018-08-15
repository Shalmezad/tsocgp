from tsocgp.validation import EachTrainIsScheduledValidator
import unittest
import json
import os

class EachTrainIsScheduledValidatorTests(unittest.TestCase):
    def test_good_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            solution = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            with open('data/sample_scenario_solution.json') as f:
                solution = json.load(f)
            validator = EachTrainIsScheduledValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}".format(results))

    
    def test_missing_train_run(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
            'id': 111
        })
        solution = {}
        solution['train_runs'] = []
        validator = EachTrainIsScheduledValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(1, len(results))

    
    def test_too_many_train_runs(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
            'id': 111
        })
        solution = {}
        solution['train_runs'] = []
        solution['train_runs'].append({
            'service_intention_id': 111
        })
        solution['train_runs'].append({
            'service_intention_id': 111
        })
        validator = EachTrainIsScheduledValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(1, len(results))

    def exactly_one_train_run(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
            'id': 111
        })
        solution = {}
        solution['train_runs'] = []
        solution['train_runs'].append({
            'service_intention_id': 111
        })
        validator = EachTrainIsScheduledValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(0, len(results))