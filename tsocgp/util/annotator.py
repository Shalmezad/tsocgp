import copy
import networkx as nx

class Annotator(object):
    """
    Annotates a given problem dictionary.

    Basically, adds fields that are useful to have (longest path length, etc)
    """
    @staticmethod
    def annotate(problem):
        annotated = copy.deepcopy(problem)
        # Alright, let's go through and annotate. 
        # 1) Quick DAG
        dags = Annotator.build_dag(problem)
        annotated['dag'] = dags[0]
        annotated['dag_nx'] = dags[1]
        annotated['start_nodes'] = dags[2]
        # 2) longest_length
        # Each route needs it's longest length...
        for route in annotated['routes']:
            i = route['id']
            path = nx.dag_longest_path(annotated['dag_nx'][i])
            temp_l = len(path)
            route['longest_length'] = temp_l
        l = Annotator.longest_length(annotated['dag_nx'])
        annotated['longest_length'] = l

        return annotated

    @staticmethod
    def longest_length(dags_nx):
        l = 0
        for route_id, graph in dags_nx.items():
            path = nx.dag_longest_path(graph)
            temp_l = len(path)
            if temp_l > l:
                l = temp_l
        return l

    @staticmethod
    def build_dag(problem):
        route_graphs_nx = dict()
        route_graphs = dict()
        start_nodes = dict()
        for route in problem["routes"]:
            G = nx.DiGraph(route_id = route["id"], name="Route-Graph for route "+str(route["id"]))
            dag = dict()
            start_node_list = []
            for path in route["route_paths"]:
                for (i, route_section) in enumerate(path["route_sections"]):
                    sn = route_section['sequence_number']
                    fni = Annotator.from_node_id(path, route_section, i)
                    tni = Annotator.to_node_id(path, route_section, i)
                    if i == 0 and "route_alternative_marker_at_entry" not in route_section.keys():
                        start_node_list.append(fni)
                    if fni not in dag:
                        dag[fni] = []
                    dag[fni].append(tni)
                    G.add_edge(Annotator.from_node_id(path, route_section, i),
                            Annotator.to_node_id(path, route_section, i),
                            sequence_number=sn)
            route_graphs[route["id"]] = dag
            route_graphs_nx[route["id"]] = G
            start_nodes[route["id"]] = start_node_list
        return (route_graphs, route_graphs_nx, start_nodes)

    @staticmethod
    def from_node_id(route_path, route_section, index_in_path):
        """
        Borrowed from route_graph.py
        """
        if "route_alternative_marker_at_entry" in route_section.keys() and \
                route_section["route_alternative_marker_at_entry"] is not None and \
                len(route_section["route_alternative_marker_at_entry"]) > 0:
                    return "(" + str(route_section["route_alternative_marker_at_entry"][0]) + ")"
        else:
            if index_in_path == 0:  # can only get here if this node is a very beginning of a route
                return "(" + str(route_section["sequence_number"]) + "_beginning)"
            else:
                return "(" + (str(route_path["route_sections"][index_in_path - 1]["sequence_number"]) + "->" +
                            str(route_section["sequence_number"])) + ")"

    @staticmethod
    def to_node_id(route_path, route_section, index_in_path):
        """
        Borrowed from route_graph.py
        """
        if "route_alternative_marker_at_exit" in route_section.keys() and \
                route_section["route_alternative_marker_at_exit"] is not None and \
                len(route_section["route_alternative_marker_at_exit"]) > 0:

                    return "(" + str(route_section["route_alternative_marker_at_exit"][0]) + ")"
        else:
            if index_in_path == (len(route_path["route_sections"]) - 1): # meaning this node is a very end of a route
                return "(" + str(route_section["sequence_number"]) + "_end" + ")"
            else:
                return "(" + (str(route_section["sequence_number"]) + "->" +
                            str(route_path["route_sections"][index_in_path + 1]["sequence_number"])) + ")"