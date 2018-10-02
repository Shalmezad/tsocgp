from tsocgp.validation import PassThroughAllSectionRequirementsValidator
import unittest
import json
import os

class PassThroughAllSectionRequirementsValidatorTests(unittest.TestCase):
    def test_good_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            solution = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            with open('data/sample_scenario_solution.json') as f:
                solution = json.load(f)
            validator = PassThroughAllSectionRequirementsValidator()
            results = validator.validate(problem, solution)
            self.assertEqual(0, len(results), msg="An error was found: {}".format(results))

    def test_section_requirements_missed(self):
        problem = {}
        problem['service_intentions'] = []
        problem['service_intentions'].append({
			"id": 111,
            "section_requirements": [{
                "section_marker": "A"
            },{
                "section_marker": "B"
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
        validator = PassThroughAllSectionRequirementsValidator()
        results = validator.validate(problem, solution)
        # We missed 1 requirement (B)
        self.assertEqual(1, len(results))    