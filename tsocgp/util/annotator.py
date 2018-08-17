import copy

class Annotator(object):
    """
    Annotates a given problem dictionary.

    Basically, adds fields that are useful to have (longest path length, etc)
    """
    @staticmethod
    def annotate(problem):
        annotated = copy.deepcopy(problem)
        return annotated