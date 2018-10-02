from tsocgp.validation import Validator 

class PassThroughAllSectionRequirementsValidator(Validator):
    """
    Consistency Rule #6
    pass through all *section_requirements* 
    a *train_run_section* references a *section_requirement* if and only if 
    this *section_requirement* is listed in the *service_intention*.
    for example, in the [sample solution](../sample_files/sample_scenario_solution.json), 
    the *train_run_sections* for *service_intention* 111 have references to the *section_requirements* A, B and C.
    But the *train_run_sections* for *service_intention* 113 only reference *section_requirements* A and C: 
    This is because in the [sample instance](../sample_files/sample_scenario.json) 
    the *service_intention* for 113 does not __have__ a *section_requirement* for the *section_marker* 'B', 
    but only for 'A' and 'C'
    """
    def rule_name(self):
        return "pass through all *section_requirements*"

    def validate(self, problem, solution):
        errors = []
        # Alright, now the fun...
        #TODO: Code me
        # Go through the problem's service_intentions
        for service_intention in problem["service_intentions"]:
            id = service_intention['id']
            # Go through the requirements:
            for requirement in service_intention["section_requirements"]:
                # Get the marker:
                marker = requirement["section_marker"]
                # See if it's in the solution:
                flag = False
                for train_run in solution['train_runs']:
                    if train_run['service_intention_id'] == id:
                        # Alright, find it's section
                        for section in train_run['train_run_sections']:
                            if section['section_requirement'] == marker:
                                flag = True
                                break
                if not flag:
                    # Missing a requirement:
                    errors.append(
                        self.build_error("Service ({}) section ({}) was not present in solution"
                        .format(id, marker)))

        return errors


