from tsocgp.validation import Validator 

class TimeWindowsForEarliestRequirementsValidator(Validator):
    """
    Planning Rule #102
    Time windows for *earliest*-requirements
    If a *section_requirement* specifies an *entry_earliest* and/or *exit_earliest* time, 
    then the event times for the *entry_event* and/or *exit_event* on the corresponding *train_run_section* __MUST__ be >= the specified time
    for example, in the [sample instance](../sample_files/sample_scenario.json) 
    for *service_intention* 111 there is a requirement for *section_marker* 'A' with an *entry_earliest* of 08:20:00. 
    Correspondingly, in the [sample solution](../sample_files/sample_scenario_solution.json) 
    the corresponding *entry_event* is scheduled at precisely 08:20:00. This is allowed. 
    But 08:19:59 or earlier would not be allowed; such a solution would be rejected. 
    """
    def rule_name(self):
        return "Time windows for *earliest*-requirements"

    def validate(self, problem, solution):
        errors = []

        return errors