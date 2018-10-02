import math
from tsocgp.util import TimeUtil 

# This whole thing's convoluted. 
# Needs a refactor...
# I'm thinking, divide it into 3 main parts
# 1) The DAG path builder, only relies on "route" in the chromosome
# 2) The time solver, relies on the DAG path and "delta" in the genome
# 3) The builder, takes the 2 above, makes it a usable solution

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
        route_section = SolutionBuilder.route_path_with_sequence_number(annotated_problem, route_id, sequence_number)

        train_run_section = {
            "route":route_id,
            "route_section_id": "{}#{}".format(route_id, sequence_number),
		    "sequence_number": 1,
            "route_path": sequence_number
        }
        if "section_marker" in route_section:
            marker = route_section["section_marker"][0]
            train_run_section["section_requirement"] = marker
            # There's a marker, see if we can find the entry_earliest requirement:
            requirement = SolutionBuilder.section_requirement_with_marker(annotated_problem,route_id,marker)
            if "entry_earliest" in requirement:
                current_time = TimeUtil.hms_to_seconds_since_midnight(requirement["entry_earliest"])
                train_run_section["entry_time"] = TimeUtil.seconds_since_midnight_to_hms(current_time)
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
            if sequence_number:
                route_section = SolutionBuilder.route_path_with_sequence_number(annotated_problem, route_id, sequence_number)
            else:
                route_section = SolutionBuilder.route_path_with_alternative_name(annotated_problem, route_id, m_number)
                sequence_number = route_section["sequence_number"]
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
    def route_path_with_sequence_number(annotated_problem, route_id, sequence_number):
        route_section = None
        for route in annotated_problem["routes"]:
            if route["id"] != route_id:
                continue
            for route_path in route["route_paths"]:
                for rs in route_path["route_sections"]:
                    if rs["sequence_number"] == sequence_number:
                        route_section = rs
        return route_section

    @staticmethod
    def route_path_with_alternative_name(annotated_problem, route_id, alt_name):
        route_section = None
        for route in annotated_problem["routes"]:
            if route["id"] != route_id:
                continue
            for route_path in route["route_paths"]:
                for rs in route_path["route_sections"]:
                    if "route_alternative_marker_at_entry" in rs and alt_name in rs["route_alternative_marker_at_entry"]:
                        route_section = rs
        return route_section

    
    @staticmethod
    def section_requirement_with_marker(annotated_problem, route_id, marker):
        section_requirement = None
        for service_intentions in annotated_problem["service_intentions"]:
            if service_intentions["route"] != route_id:
                continue
            for sr in service_intentions["section_requirements"]:
                if sr["section_marker"] == marker:
                    section_requirement = sr
        return section_requirement
    
    @staticmethod
    def select_from_list(l, perc):
        index = math.floor(len(l) * perc)
        return l[index]