from tsocgp.validation import Validator 
from collections import Counter

class MinimumSectionTimeValidator(Validator):
    """
    Planning rule #103
    Minimum section time
    For each *train_run_section* the following holds: 
    t_exit - t_entry >= minimum_running_time + min_stopping_time, 
    where t_entry, t_exit are the entry and exit times into this *train_run_section*, 
    *minimum_running_time* is given by the *route_section* corresponding to this *train_run_section* 
    and *min_stopping_time* is given by the *section_requirement* 
    corresponding to this *train_run_section* or equal to 0 (zero) if no *section_requirement* with a *min_stopping_time* is associated to this *train_run_section*. 
    """
    def rule_name(self):
        return "Minimum section time"

    def validate(self, problem, solution):
        errors = []
        # TODO: Code me

        return errors