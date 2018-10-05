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
        dags = SolutionBuilder.build_dag_paths_from_genome(problem, genome)
        for intention in problem["service_intentions"]:
            i = intention["id"]
            chromosome = genome.chromosomes[i]
            train_run = SolutionBuilder.train_run_from_dag(problem, chromosome, dags[i], i)
            s["train_runs"].append(train_run)
        return s


    @staticmethod
    def train_run_from_dag(annotated_problem, chromosome, dag_path, route_id):
        # Dag_path should be the array of nodes:
        train_run = {}
        train_run["service_intention_id"] = route_id
        train_run["train_run_sections"] = []
        c_idx = 0
        current_time = 0
        #print(dag_path)
        for node in dag_path:
            temp_node = node.strip("(").strip(")")
            sequence_number = None
            m_number = None
            # Try and parse out sequence or m_number
            if "->" in temp_node:
                sequence_number = int(temp_node.split('->', 1)[1])
            elif "_end" in temp_node:
                sequence_number = int(temp_node.strip("_end"))
            elif "_beginning" in temp_node:
                sequence_number = int(temp_node.strip("_beginning"))
            else:
                m_number = temp_node
            # Try and find the route section:
            route_section = None
            if sequence_number:
                route_section = SolutionBuilder.route_path_with_sequence_number(annotated_problem, route_id, sequence_number)
            else:
                route_section = SolutionBuilder.route_path_with_alternative_name(annotated_problem, route_id, m_number)
                if route_section:
                    sequence_number = route_section["sequence_number"]
            if not route_section:
                raise ValueError("Unable to find route section with node: ({})".format(node))
            # Build the train_run_section:
            train_run_section = {
                "route":route_id,
                "route_section_id": "{}#{}".format(route_id, sequence_number),
                "sequence_number": c_idx + 1,
                "route_path": sequence_number
            }
            if "section_marker" in route_section:
                marker = route_section["section_marker"][0]
                train_run_section["section_requirement"] = marker
                # There's a marker, see if we can find the entry_earliest requirement:
                requirement = SolutionBuilder.section_requirement_with_marker(annotated_problem,route_id,marker)
                if requirement and "entry_earliest" in requirement:
                    current_time = TimeUtil.hms_to_seconds_since_midnight(requirement["entry_earliest"])
            else: 
                train_run_section["section_requirement"] = None
            train_run_section["entry_time"] = TimeUtil.seconds_since_midnight_to_hms(current_time)
            min_time = 0
            if "minimum_running_time" in route_section:
                min_time = TimeUtil.ddi_duration_to_seconds(route_section["minimum_running_time"])
            current_time += min_time
            current_time += chromosome[c_idx]['delta']
            train_run_section["exit_time"] = TimeUtil.seconds_since_midnight_to_hms(current_time)
            # TODO: Figure out our exit time
            train_run["train_run_sections"].append(train_run_section)
            c_idx += 1
        return train_run
            



    @staticmethod
    def build_dag_paths_from_genome(annotated_problem, genome):
        paths = {}
        for intention in annotated_problem["service_intentions"]:
            i = intention["id"]
            chromosome = genome.chromosomes[i]
            paths[i] = SolutionBuilder.build_dag_path_from_chromosome(annotated_problem,chromosome,i)
        return paths


    @staticmethod
    def build_dag_path_from_chromosome(annotated_problem, chromosome, route_id):
        """
        Given the problem, chromosome, and route_id,
        This will figure out the path of sections the chromosome represents
        ie: ["1_beginning","M1", "4->5", "M2", "7->8", "8->9", "9_end"]
        """
        path = []
        start_nodes = annotated_problem['start_nodes'][route_id]
        start_node = SolutionBuilder.select_from_list(start_nodes, chromosome[0]['route'])
        path.append(start_node)
        cur_node = start_node
        c_idx = 1
        while cur_node in annotated_problem['dag'][route_id]:
            nodes = annotated_problem['dag'][route_id][cur_node]
            cur_node = SolutionBuilder.select_from_list(nodes, chromosome[c_idx]['route'])
            c_idx = c_idx + 1
            path.append(cur_node)
        return path

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