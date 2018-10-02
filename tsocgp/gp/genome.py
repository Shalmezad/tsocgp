import random
class Genome(object):
    """
    A genome consists of a dictionary of chromosomes
    where the key is the train section id,
    and the value is a chromosome.

    A chromosome is an array of genes.

    A gene is a % marking which path to take, and a delta for the time beyond earliest_exit to leave.
    For the %:
        If there are 2 paths, < 50% would be the top path, >= 50% would be the bottom path.
        If there are 3 paths, < 33% would be the top path, < 66% would be the middle path, etc
        etc
    For the delta:
        If an earliest exit for the section exists, it's the number of seconds beyond that to wait.
        If not, it's the ammount of time to wait.
    """
    def __init__(self):
        self.chromosomes = {}

    def genesis(self, annotated_problem):
        # Reset genes to nothing:
        self.chromosomes = {}
        for route in annotated_problem['routes']:
            self.chromosomes[route['id']] = Genome.build_chromosome_for_annotated_route(route)

    def __hash__(self):
        return hash(frozenset(self.chromosomes.items()))
        #return hash(self.chromosomes)

    @staticmethod
    def build_chromosome_for_annotated_route(route):
        # It's annotated so:
        length = route['longest_length']
        genes = []
        for _ in range(length):
            genes.append(Genome.build_gene())
        return genes

    @staticmethod
    def build_gene():
        gene = {}
        gene['route'] = random.random()
        gene['delta'] = random.randint(0,10000)
        return gene