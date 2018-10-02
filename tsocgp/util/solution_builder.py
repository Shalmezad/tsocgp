import math
class SolutionBuilder(object):
    """
    Main purpose is to build a dictionary solution from a problem and a genome:
    """
    @staticmethod
    def build_solution(problem, genome):
        """
        Builds a submittable solution from the provided genome
        """
        s = {}
        # There are 4 main keys we need:
        #"problem_instance_label": "SBB_challenge_sample_scenario_with_routing_alternatives",
        #"problem_instance_hash": -1254734547,
        #"hash": 1538680897,
        #"train_runs": 
        s["problem_instance_label"] = problem["label"]
        s["problem_instance_hash"] = problem["hash"]
        # TODO: Implement hash
        #s["hash"] = hash(genome)
        s["train_runs"] = []
        for intention in problem["service_intentions"]:
            i = intention["id"]
            chromosome = genome.chromosomes[i]
            train_run = SolutionBuilder.build_train_run(problem, chromosome, i)
            s["train_runs"].append(train_run)
        return s

    @staticmethod
    def build_train_run(annotated_problem, chromosome, route_id):
        train_run = {}
        train_run["service_intention_id"] = route_id
        train_run["train_run_sections"] = []
        # TODO: Loop over chromosome, add in pieces
        # Alright, let's see what node we start with:
        start_nodes = annotated_problem['start_nodes'][route_id]
        start_node = SolutionBuilder.select_from_list(start_nodes, chromosome[0]['route'])
        cur_node = start_node
        next_nodes = annotated_problem['dag'][route_id][start_node]
        current_time = 0 # Time in seconds since 00:00:00
        # Add this:
        #        {
		#			 "entry_time": "08:20:00",
		#			 "exit_time": "08:20:53",
		#			 "route": 111,
		#			 "route_section_id": "111#3",
		#			 "sequence_number": 1,
		#			 "route_path": 3,
		#			 "section_requirement": "A"
		#		},
        sequence_number = int(cur_node.strip("(").strip("_beginning)"))
        # Find the route section with this sequence...
        route_section = None
        for route in annotated_problem["routes"]:
            if route["id"] != route_id:
                continue
            for route_path in route["route_paths"]:
                for rs in route_path["route_sections"]:
                    if rs["sequence_number"] == sequence_number:
                        route_section = rs
        train_run_section = {
            "route":route_id,
            "route_section_id": "{}#{}".format(route_id, sequence_number),
		    "sequence_number": 1,
            "route_path": sequence_number
        }
        if "section_marker" in route_section:
            train_run_section["section_requirement"] = route_section["section_marker"][0]
            # There's a marker, see if we can find the entry_earliest requirement:
            # TODO: Code me
        else: 
            train_run_section["section_requirement"] = None
        train_run["train_run_sections"].append(train_run_section)
        # Then loop until we don't have anywhere to go
        c_idx = 1
        while cur_node in annotated_problem['dag'][route_id]:
            # Move our cur_node
            next_nodes = annotated_problem['dag'][route_id][cur_node]
            cur_node = SolutionBuilder.select_from_list(next_nodes, chromosome[c_idx]['route'])
            # Add it to the list
            # TODO: Code me
            # So, we either have a MX, a X->Y, or a X_end node...
            temp_node = cur_node.strip("(").strip(")")
            sequence_number = None
            m_number = None
            if "->" in temp_node:
                sequence_number = int(temp_node.split('->', 1)[0])
            elif "_end" in temp_node:
                sequence_number = int(temp_node.strip("_end"))
            else:
                m_number = temp_node

            # Find the route section with this sequence...
            route_section = None
            for route in annotated_problem["routes"]:
                if route["id"] != route_id:
                    next
                for route_path in route["route_paths"]:
                    for rs in route_path["route_sections"]:
                        if sequence_number:
                            if rs["sequence_number"] == sequence_number:
                                route_section = rs
                        if m_number:
                            if "route_alternative_marker_at_entry" in rs and m_number in rs["route_alternative_marker_at_entry"]:
                                route_section = rs
            if not route_section:
                raise ValueError("Unable to find route section with node: ({})".format(cur_node))
            train_run_section = {
                "route":route_id,
                "route_section_id": "{}#{}".format(route_id, sequence_number),
                "sequence_number": c_idx + 1,
                "route_path": sequence_number
            }
            if "section_marker" in route_section:
                train_run_section["section_requirement"] = route_section["section_marker"][0]
            else: 
                train_run_section["section_requirement"] = None
            train_run["train_run_sections"].append(train_run_section)
                
            # Shift pointers
            c_idx = c_idx + 1


        return train_run

    
    @staticmethod
    def select_from_list(l, perc):
        index = math.floor(len(l) * perc)
        return l[index]