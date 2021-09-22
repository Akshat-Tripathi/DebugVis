from typing import List
from collections.abc import Iterable

BEST_COLOUR = "blue"
PRIMITIVES = (int, str, bool, float)


def is_primitive(type_):
    return type(type_) in PRIMITIVES


def is_collection(type_):
    return isinstance(type_, Iterable)


class ListCollection:
    def __init__(self, type_, items):
        self.label = type_.__name__
        self.items = items

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


class Null:
    def __str__(self):
        return "Null"

    def __repr__(self):
        return "Null"


def derive_graph(obj, field_filter=lambda f: False,
                 ignore_collections=True, node_colour_func=lambda x: BEST_COLOUR,
                 edge_colour_func=lambda a, b: BEST_COLOUR, label_func=str) -> str:
    """
    Automatically derives the appropriate json data for a given object.
    field_filter - returns True iff the field should not be shown the resulting diagram
    ignore_collections - if set to False, then all collections will be linked to an intermediate node
    node_colour_func - takes an object and returns its colour
    edge_colour_func - takes a pair of objects and returns the colour of the edge connecting them
    label_func - takes an object and returns its label
    """
    def _dfs(obj, visited, links):
        if obj in visited:
            return
        visited.add(obj)
        for (name, value) in obj.__dict__.items():
            if field_filter(name) or is_primitive(value):
                pass
            elif is_collection(value):
                if ignore_collections:
                    dummy = ListCollection(type(value), value)
                    visited.add(dummy)
                    links.add((obj, dummy))
                    obj = dummy
                for v in value:
                    v = Null() if v is None else v
                    links.add((obj, v))
                    _dfs(v, visited=visited, links=links)
            else:
                value = Null() if value is None else value
                links.add((obj, value))
                _dfs(value, visited=visited, links=links)

    visited = set()
    links = set()
    _dfs(obj, visited, links)

    nodes = [
        {"id": str(id(v)), "label": label_func(v), "color": node_colour_func(v)} for v in visited
    ]

    edges = [
        {"from": str(id(from_)), "to": str(id(to)), "color": edge_colour_func(from_, to)} for (from_, to) in links
    ]

    return str({
        "kind": {"graph": True},
        "nodes": nodes,
        "edges": edges
    }).replace("\'", "\"").replace("True", "true")
