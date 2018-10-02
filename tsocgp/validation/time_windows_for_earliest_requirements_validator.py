from tsocgp.validation import Validator 
from datetime import datetime, time,date

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

        # Go through each service_intentions in the problem:
        for service_intention in problem['service_intentions']:
            # We need the id to refer to in the solution:
            id = service_intention['id']
            # Go through each of the section requirements:
            for requirement in service_intention['section_requirements']:
                # Get the section marker to refer to in the problem:
                marker = requirement['section_marker']
                # Does it have an entry_earliest?
                if 'entry_earliest' in requirement:
                    entry_earliest = datetime.strptime(requirement['entry_earliest'],"%H:%M:%S")
                    # Alright, we have what it should be. What was it in the solution?
                    for train_run in solution['train_runs']:
                        if train_run['service_intention_id'] == id:
                            # Alright, find it's section
                            for section in train_run['train_run_sections']:
                                if section['section_requirement'] == marker:
                                    if 'entry_time' not in section:
                                        # TODO: See if this key is required by another rule. If so, remove this error
                                        errors.append(
                                            self.build_error("Service ({}) section ({}) did not have an entry_time"
                                            .format(id, marker)))
                                        continue
                                    # Alright, get the entry time:
                                    entry_time = datetime.strptime(section['entry_time'],"%H:%M:%S")
                                    if entry_time < entry_earliest:
                                        # FAILED!
                                        errors.append(
                                            self.build_error("Service ({}) section ({}) failed to meet entry earliest requirement"
                                            .format(id, marker)))

                # Does it have an exit_earliest?
                if 'exit_earliest' in requirement:
                    exit_earliest = datetime.strptime(requirement['exit_earliest'],"%H:%M:%S")
                    # Alright, we have what it should be. What was it in the solution?
                    for train_run in solution['train_runs']:
                        if train_run['service_intention_id'] == id:
                            # Alright, find it's section
                            for section in train_run['train_run_sections']:
                                if section['section_requirement'] == marker:
                                    # Alright, get the entry time:
                                    exit_time = datetime.strptime(section['exit_time'],"%H:%M:%S")
                                    if exit_time < exit_earliest:
                                        # FAILED!
                                        errors.append(
                                            self.build_error("Service ({}) section ({}) failed to meet exit earliest requirement"
                                            .format(id, marker)))

        return errors