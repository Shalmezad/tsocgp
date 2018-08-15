from tsocgp.validation import Validator 

class ProblemInstanceHashPresentValidator(Validator):
    """
    Consistency Rule #1
    problem_instance_hash present
    the field *problem_instance_hash* is present in the solution 
    and has the correct value 
    (namely that of the problem instance that this solution refers to)
    """
    def rule_name(self):
        return "problem_instance_hash present"

    def validate(self, problem, solution):
        errors = []
        # 1) See if the hash is present:
        if 'problem_instance_hash' not in solution:
            errors.append(self.build_error("Missing key: 'problem_instance_hash'"))
        else:
            # 2) See if it matches:
            problem_key = problem['hash']
            solution_key = solution['problem_instance_hash']
            if problem_key != solution_key:
                errors.append(
                    self.build_error("Solution key ({}) did not match problem key ({})"
                                        .format(solution_key, problem_key)))
        return errors