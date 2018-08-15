class Validator(object):
    """
    A generic validator for a solution to a given problem
    Will return an array of issues that occured.

    NOTE: These work on RAW problem/solution hashes (ie: if you did json.load(file))
    """
    def validate(self, problem, solution):
        raise NotImplementedError()

    def rule_name(self):
        raise NotImplementedError()

    def build_error(self, issue):
        return {
            "rule_name": self.rule_name(),
            "issue": issue
        }
