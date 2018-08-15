from tsocgp.validation import TimeWindowsForEarliestRequirementsValidator
import unittest
import json
import os

class TimeWindowsForEarliestRequirementsValidatorTests(unittest.TestCase):
    def test_good_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            solution = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            with open('data/sample_scenario_solution.json') as f:
                solution = json.load(f)
            validator = TimeWindowsForEarliestRequirementsValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}".format(results))

    def test_no_early_requirements(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
			"id": 111,
            "section_requirements": [] # No requirements at all
        })
        solution = {}
        validator = TimeWindowsForEarliestRequirementsValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(0, len(results))    


    def test_entry_early_requirements_missed(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
			"id": 111,
            "section_requirements": [{
                "section_marker": "A",
                "entry_earliest": "08:20:00"
            }]
        })
        solution = {
            "train_runs": [{
                "service_intention_id": 111,
                "train_run_sections": [{
                        "entry_time": "08:19:59", #But 08:19:59 or earlier would not be allowed
                        "exit_time": "08:20:53",
                        "route": 111,
                        "route_section_id": "111#3",
                        "sequence_number": 1,
                        "route_path": 3,
                        "section_requirement": "A"
                    }]
            }]
        }
        validator = TimeWindowsForEarliestRequirementsValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(1, len(results))    

    def test_entry_early_requirements_exact(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
			"id": 111,
            "section_requirements": [{
                "section_marker": "A",
                "entry_earliest": "08:20:00"
            }]
        })
        solution = {
            "train_runs": [{
                "service_intention_id": 111,
                "train_run_sections": [{
                        "entry_time": "08:20:00",
                        "exit_time": "08:20:53",
                        "route": 111,
                        "route_section_id": "111#3",
                        "sequence_number": 1,
                        "route_path": 3,
                        "section_requirement": "A"
                    }]
            }]
        }
        validator = TimeWindowsForEarliestRequirementsValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(0, len(results))    

    def test_exit_early_requirements_missed(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
			"id": 111,
            "section_requirements": [{
                "section_marker": "A",
                "exit_earliest": "08:20:00"
            }]
        })
        solution = {
            "train_runs": [{
                "service_intention_id": 111,
                "train_run_sections": [{
                        "entry_time": "08:15:00", 
                        "exit_time": "08:19:59",
                        "route": 111,
                        "route_section_id": "111#3",
                        "sequence_number": 1,
                        "route_path": 3,
                        "section_requirement": "A"
                    }]
            }]
        }
        validator = TimeWindowsForEarliestRequirementsValidator()
        results = validator.validate(problem, solution)
        self.assertEqual(1, len(results))    