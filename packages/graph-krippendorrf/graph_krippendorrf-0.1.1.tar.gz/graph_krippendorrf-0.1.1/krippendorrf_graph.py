import json
from pathlib import Path

import numpy as np
import networkx as nx
from tqdm import tqdm


def nominal_metric(a, b):
    return a != b


def graph_overlap_metric(a, b):
    return len(a & b) == 0


def graph_edit_distance(a, b):
    return compute_normalized_graph_edit_distance(a, b)


def instantiate_networkx_graph(triples: list[tuple]):
    G = nx.DiGraph()
    for (subj, rel, obj) in triples:
        G.add_edge(subj, obj, relation=rel)
    return G


def compute_normalized_graph_edit_distance(triples_1: list[tuple], triples_2: list[tuple]):
    g0 = nx.empty_graph()
    g1 = instantiate_networkx_graph(triples_1)
    g2 = instantiate_networkx_graph(triples_2)
    normalized_ged = nx.graph_edit_distance(g1, g2)/(nx.graph_edit_distance(g1, g0)+nx.graph_edit_distance(g2, g0))
    return normalized_ged


def interval_metric(a, b):
    return ( a -b )**2


def ratio_metric(a, b):
    return (( a -b ) /( a +b) )**2


def compute_alpha(data, metric=interval_metric, force_vecmath=False, convert_items=float, missing_items=None, distance_matrix_path=None):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items

    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    convert_items: function for the type conversion of items (default: float)
    missing_items: indicator for missing items (default: None)
    '''

    # number of coders
    m = len(data)

    # set of constants identifying missing values
    if missing_items is None:
        maskitems = []
    else:
        maskitems = list(missing_items)
    if np is not None:
        maskitems.append(np.ma.masked_singleton)

    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.items()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)

        for it, g in diter:
            if g not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                its.append(convert_items(g))

    units = dict((it, d) for it, d in units.items() if len(d) > 1)  # units with pairable values

    n = sum(len(pv) for pv in units.values())  # number of pairable values
    if n == 0:
        raise ValueError("No items to compare.")

    np_metric = (np is not None) and ((metric in (interval_metric, nominal_metric, ratio_metric)) or force_vecmath)

    Do = 0. # disagreement observed

    if metric == graph_edit_distance:
        if distance_matrix_path is not None and Path(distance_matrix_path).exists():
            with open(distance_matrix_path, "r") as f:
                graph_distance_dict = json.load(f)
        else:
            graph_distance_dict = {}
            for grades in tqdm(units.values()):
                for gj in grades:
                    for gi in grades:
                        key = str(gi)+str(gj)
                        if key not in graph_distance_dict:
                            if str(gi) == str(gj):
                                graph_distance_dict[key] = 0
                            else:
                                graph_distance_dict[key] = metric(gi, gj)

    for grades in units.values():
        if np_metric:
            gr = np.asarray(grades)
            Du = sum(np.sum(metric(gr, gri)) for gri in gr)
        else:
            if metric == graph_edit_distance:
                Du = sum(graph_distance_dict[str(gi)+str(gj)] for gi in grades for gj in grades)
            else:
                Du = sum(metric(gi, gj) for gi in grades for gj in grades)

        Do += Du /float(len(grades ) -1)

    Do /= float(n)
    if Do == 0:
        return 1.

    De = 0. # disagreement expected by chance
    for g1 in units.values():
        if np_metric:
            d1 = np.asarray(g1)
            for g2 in units.values():
                De += sum(np.sum(metric(d1, gj)) for gj in g2)
        else:
            for g2 in units.values():
                if metric == graph_edit_distance:
                    for gi in g1:
                        for gj in g2:
                            if str(gi)+str(gj) not in graph_distance_dict:
                                graph_distance_dict[str(gi) + str(gj)] = metric(gi, gj)
                    De += sum(graph_distance_dict[str(gi)+str(gj)] for gi in g1 for gj in g2)
                else:
                    De += sum(metric(gi, gj) for gi in g1 for gj in g2)
    De /= float(n * (n-1))
    if distance_matrix_path is None:
        with open("./graph_distance_matrix.json", "w") as f:
            json.dump(graph_distance_dict, f)
    else:
        with open(distance_matrix_path, "w") as f:
            json.dump(graph_distance_dict, f)
    return 1.-Do/De if (Do and De) else 1.


if __name__ == '__main__':
    data = [
        [
            {('Monetary Policy', 'Increases', 'Inflation')},
            {('Wages', 'Increases', 'Inflation')},
            {('Energy Prices', 'Increases', 'Inflation'), ('Medical Costs', 'Increases', 'Inflation'), ('Tax Increases', 'Increases', 'Inflation')},
            {('Demand (residual)', 'Increases', 'Wages'), ('Wages', 'Increases', 'Inflation')},
            {('Government Debt', 'Increases', 'Inflation'), ('Monetary Policy', 'Decreases', 'Inflation')},
            {('Tax Increases', 'Increases', 'Inflation'), ('Wages', 'Increases', 'Inflation Expectations')},
            {('Government Debt', 'Increases', 'Inflation'), ('Monetary Policy', 'Decreases', 'Government Debt')},
            {('Energy Prices', 'Increases', 'Inflation'), ('Food Prices', 'Increases', 'Inflation'), ('Food Prices', 'Increases', 'Inflation Expectations'), ('Medical Costs', 'Increases', 'Inflation'), ('Supply (residual)', 'Increases', 'Inflation')},
            {('Pent-up Demand', 'Increases', 'Inflation')}, {('Wages', 'Increases', 'Inflation')}],
        [
            {('Monetary Policy', 'Increases', 'Inflation')},
            {('Wages', 'Increases', 'Inflation')},
            {('Energy Prices', 'Increases', 'Inflation'),
               ('Food Prices', 'Increases', 'Inflation'),
               ('Inflation', 'Increases', 'Energy Prices'),
               ('Inflation Expectations', 'Increases', 'Inflation'),
               ('Medical Costs', 'Increases', 'Inflation'),
               ('Supply (residual)', 'Decreases', 'Inflation'),
               ('Tax Increases', 'Increases', 'Inflation'),
               ('Transportation Costs', 'Decreases', 'Inflation')},
            {('Demand (residual)', 'Increases', 'Inflation'), ('Monetary Policy', 'Decreases', 'Inflation'), ('Wages', 'Increases', 'Inflation')},
            {('Government Debt', 'Increases', 'Inflation'), ('Monetary Policy', 'Decreases', 'Inflation'), ('Pent-up Demand', 'Increases', 'Inflation'), ('Supply (residual)', 'Increases', 'Inflation')},
            {('Tax Increases', 'Increases', 'Inflation'), ('Wages', 'Increases', 'Inflation')},
            {('Government Spending', 'Increases', 'Inflation')},
            {('Energy Prices', 'Increases', 'Inflation'),
               ('Food Prices', 'Increases', 'Inflation'),
               ('Medical Costs', 'Increases', 'Inflation'),
               ('Supply (residual)', 'Increases', 'Inflation'),
               ('Transportation Costs', 'Increases', 'Inflation')},
            {('Inflation Expectations', 'Increases', 'Inflation'), ('Pent-up Demand', 'Increases', 'Inflation')},
            {('Wages', 'Increases', 'Inflation')}],
        [
            {('Monetary Policy', 'Increases', 'Inflation')},
            {('Inflation', 'Decreases', 'Monetary Policy'), ('Wages', 'Increases', 'Inflation')},
            {('Medical Costs', 'Increases', 'Inflation'), ('Tax Increases', 'Increases', 'Medical Costs'), ('War', 'Increases', 'Energy Prices')},
            {('Demand (residual)', 'Increases', 'Inflation'), ('Inflation', 'Increases', 'Wages'), ('Monetary Policy', 'Decreases', 'Demand (residual)'), ('Wages', 'Increases', 'Inflation')},
            {('Demand (residual)', 'Increases', 'Inflation'), ('Government Spending', 'Increases', 'Inflation')},
            {('Tax Increases', 'Increases', 'Inflation'), ('Wages', 'Increases', 'Inflation')},
            {('Government Spending', 'Decreases', 'Demand (residual)'), ('Government Spending', 'Increases', 'Inflation'), ('Inflation Expectations', 'Increases', 'Monetary Policy'), ('Monetary Policy', 'Decreases', 'Government Spending')},
            {('Climate', 'Increases', 'Supply (residual)'),
               ('Energy Prices', 'Increases', 'Inflation'),
               ('Food Prices', 'Increases', 'Inflation'),
               ('Medical Costs', 'Increases', 'Inflation'),
               ('Supply (residual)', 'Increases', 'Food Prices')},
            {('Pent-up Demand', 'Increases', 'Inflation')},
            {('Inflation', 'Increases', 'Wages'), ('Wages', 'Increases', 'Inflation')}],
        [
            {('Monetary Policy', 'Increases', 'Inflation')},
            {('Inflation', 'Decreases', 'Inflation')},
            {('Energy Prices', 'Increases', 'Inflation'), ('Monetary Policy', 'Increases', 'Inflation'), ('Price-Gouging', 'Increases', 'Inflation'), ('Tax Increases', 'Increases', 'Inflation')},
            {('Demand (residual)', 'Increases', 'Inflation'), ('Inflation', 'Decreases', 'Demand (residual)'), ('Inflation', 'Increases', 'Inflation')},
            {('Monetary Policy', 'Decreases', 'Inflation'), ('Monetary Policy', 'Increases', 'Inflation Expectations')},
            {('Tax Increases', 'Increases', 'Inflation'), ('Wages', 'Increases', 'Inflation')},
            {('Mismanagement', 'Increases', 'Inflation')},
            {('Energy Prices', 'Increases', 'Inflation'), ('Food Prices', 'Increases', 'Inflation')},
            {('Pent-up Demand', 'Increases', 'Inflation')},
            {('Wages', 'Increases', 'Inflation')}]
    ]

    missing = "*" # indicator for missing values

    print("Gragh edit distance: %.3f" % compute_alpha(data, graph_edit_distance, missing_items=missing, convert_items=set, distance_matrix_path="./distance_matrix.json"))
