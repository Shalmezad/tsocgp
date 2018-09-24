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
        # 2) longest_length

        return annotated

    @staticmethod
    def longest_length(dags_nx):
        l = 0
        for route_id, graph in dags_nx.items():
            path = nx.dag_longest_path(graph)
            temp_l = len(nx.dag_longest_path(graph))
            if temp_l > l:
                l = temp_l
        return l

    @staticmethod
    def build_dag(problem):
        route_graphs_nx = dict()
        route_graphs = dict()
        for route in problem["routes"]:
            G = nx.DiGraph(route_id = route["id"], name="Route-Graph for route "+str(route["id"]))
            dag = dict()
            for path in route["route_paths"]:
                for (i, route_section) in enumerate(path["route_sections"]):
                    sn = route_section['sequence_number']
                    fni = Annotator.from_node_id(path, route_section, i)
                    tni = Annotator.to_node_id(path, route_section, i)
                    if fni not in dag:
                        dag[fni] = []
                    dag[fni].append(tni)
                    G.add_edge(Annotator.from_node_id(path, route_section, i),
                            Annotator.to_node_id(path, route_section, i),
                            sequence_number=sn)
            route_graphs[route["id"]] = dag
            route_graphs_nx[route["id"]] = G
        return (route_graphs, route_graphs_nx)

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