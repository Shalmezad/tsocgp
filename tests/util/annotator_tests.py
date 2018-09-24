from tsocgp.util import Annotator
import unittest
import json
import os

class AnnotatorTests(unittest.TestCase):
    def test_dag_generation_from_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            solution = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            dags = Annotator.build_dag(problem)
            dict_dag = dags[0]
            #print(dag)
            self.assertIn(111, dict_dag)
            #self.assertEqual({}, dag)
            #validator = EachTrainIsScheduledValidator()
            #results = validator.validate(problem, solution)
            #self.assertEqual(0, len(results), msg="An error was found: {}".format(results))


    def test_longest_route_from_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            solution = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            dags = Annotator.build_dag(problem)
            dags_nx = dags[1]
            l = Annotator.longest_length(dags_nx)
            self.assertEqual(8, l)

    