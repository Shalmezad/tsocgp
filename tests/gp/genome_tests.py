from tsocgp.gp import Genome
from tsocgp.util import Annotator
import tsocgp.validation as validation
import unittest
import json
import os

class GenomeTests(unittest.TestCase):
    def test_genesis_from_file(self):
        if bool(os.environ.get('USE_SAMPLE_FILE_WHEN_TESTING', 0)):
            problem = {}
            with open('data/sample_scenario.json') as f:
                problem = json.load(f)
            annotated_problem = Annotator.annotate(problem)
            genome = Genome()
            genome.genesis(annotated_problem)
            # Should have chromosomes for both routes:
            self.assertIn(111, genome.chromosomes)
            self.assertIn(113, genome.chromosomes)
            #self.assertEqual(0, len(results), msg="An error was found: {}".format(results))

