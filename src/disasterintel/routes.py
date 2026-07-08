"""Road-network route-risk planning for emergency coordination scenarios."""

from __future__ import annotations

import networkx as nx
import pandas as pd


def build_road_graph(roads: pd.DataFrame) -> nx.Graph:
    """Build a passability-weighted road graph from synthetic road links."""
    graph = nx.Graph()
    for road in roads.itertuples(index=False):
        if int(road.is_passable) != 1:
            continue
        cost = float(road.distance) * (1.0 + 4.0 * float(road.road_risk))
        graph.add_edge(road.src_cell, road.dst_cell, distance=float(road.distance), road_risk=float(road.road_risk), cost=cost)
    return graph


def score_resource_routes(resources: pd.DataFrame, assignments: pd.DataFrame, roads: pd.DataFrame) -> pd.DataFrame:
    """Estimate shortest risk-adjusted route cost from resources to assigned cells."""
    graph = build_road_graph(roads)
    rows: list[dict] = []
    merged = assignments.merge(resources[["resource_id", "home_cell"]], on="resource_id", how="left", validate="many_to_one")
    for row in merged.itertuples(index=False):
        if row.home_cell not in graph or row.assigned_cell not in graph:
            route_cost = float("inf")
            route_distance = float("inf")
            passable = 0
        else:
            try:
                path = nx.shortest_path(graph, row.home_cell, row.assigned_cell, weight="cost")
                edges = list(zip(path[:-1], path[1:]))
                route_cost = sum(graph[u][v]["cost"] for u, v in edges)
                route_distance = sum(graph[u][v]["distance"] for u, v in edges)
                passable = 1
            except nx.NetworkXNoPath:
                route_cost = float("inf")
                route_distance = float("inf")
                passable = 0
        rows.append({
            "resource_id": row.resource_id,
            "resource_type": row.resource_type,
            "home_cell": row.home_cell,
            "assigned_cell": row.assigned_cell,
            "route_passable": passable,
            "route_distance": None if route_distance == float("inf") else round(float(route_distance), 2),
            "route_risk_adjusted_cost": None if route_cost == float("inf") else round(float(route_cost), 2),
        })
    return pd.DataFrame(rows)
