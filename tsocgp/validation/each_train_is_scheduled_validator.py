from tsocgp.validation import Validator 
from collections import Counter

class EachTrainIsScheduledValidator(Validator):
    """
    Consistency Rule #2
    each train is scheduled
    For every *service_intention* in the _problem_instance_, 
    there is exactly one *train_run* in the solution
    """
    def rule_name(self):
        return "each train is scheduled"

    def validate(self, problem, solution):
        errors = []
        # Go through problem, gather all service_intention ids:
        service_intention_ids = [d['id'] for d in problem['service_intentions']]
        # Now, go through and get all train_run ids in the solution:
        train_run_ids = [d['service_intention_id'] for d in solution['train_runs']]

        # Count occourances in train_run_ids:
        counter = Counter(train_run_ids)
        # Go through each service intention in the problem instance:
        for service_id in service_intention_ids:
            # We must have exactly one:
            if counter[service_id] != 1:
                errors.append(
                    self.build_error("Service ({}) has the wrong number of train_runs ({}) in the solution"
                                        .format(service_id, counter[service_id])))

        return errors