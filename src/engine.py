from typing import List, Dict, Any
from src.models import Shipment, Route

def calculate_route_score(route: Route, weights: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Calculates a composite penalty score for a route based on cost, transit time, delay risk, and congestion.
    Lower score = better route.
    """
    if weights is None:
        weights = {
            "cost": 0.4,
            "time": 0.3,
            "delay_prob": 0.15,
            "congestion": 0.15
        }
    
    total_cost = sum(leg.cost for leg in route.legs)
    total_time = sum(leg.time for leg in route.legs)
    avg_delay = sum(leg.delay_prob for leg in route.legs) / len(route.legs) if route.legs else 0
    avg_congestion = sum(leg.congestion for leg in route.legs) / len(route.legs) if route.legs else 0

    # Composite weighted penalty score
    score = (
        weights["cost"] * total_cost +
        weights["time"] * (total_time * 50) +  # scale hours to match cost units
        weights["delay_prob"] * (avg_delay * 1000) +
        weights["congestion"] * (avg_congestion * 1000)
    )

    return {
        "route_id": route.route_id,
        "score": round(score, 2),
        "total_cost": total_cost,
        "total_time": total_time,
        "avg_delay_risk": round(avg_delay, 2),
        "avg_congestion": round(avg_congestion, 2)
    }

def recommend_best_route(shipment: Shipment) -> Dict[str, Any]:
    """
    Evaluates all routes for a shipment and selects the one with the lowest penalty score.
    """
    evaluations = [calculate_route_score(route) for route in shipment.candidates]
    sorted_routes = sorted(evaluations, key=lambda x: x["score"])
    best_route = sorted_routes[0]

    explanation = (
        f"Route '{best_route['route_id']}' is selected as the optimal choice with a score of {best_route['score']}. "
        f"It balances cost (${best_route['total_cost']}), transit time ({best_route['total_time']} hrs), "
        f"and low risk (delay prob: {best_route['avg_delay_risk']}, congestion: {best_route['avg_congestion']})."
    )

    return {
        "shipment_id": shipment.shipment_id,
        "recommended_route": best_route,
        "all_evaluations": sorted_routes,
        "explanation": explanation
    }