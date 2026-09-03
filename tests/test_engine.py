import pytest
from src.models import Leg, Route, Shipment
from src.engine import calculate_route_score, recommend_best_route

def test_leg_validation():
    leg = Leg(**{
        "from": "Mombasa",
        "to": "Nairobi",
        "cost": 500.0,
        "time": 8.0,
        "delay_prob": 0.1,
        "congestion": 0.2,
        "geopolitical": 0.0
    })
    assert leg.from_location == "Mombasa"
    assert leg.to_location == "Nairobi"

def test_route_aggregation():
    leg1 = Leg(**{"from": "A", "to": "B", "cost": 100, "time": 2, "delay_prob": 0.1, "congestion": 0.1, "geopolitical": 0.0})
    leg2 = Leg(**{"from": "B", "to": "C", "cost": 200, "time": 4, "delay_prob": 0.3, "congestion": 0.3, "geopolitical": 0.0})
    route = Route(route_id="R1", legs=[leg1, leg2])
    route.aggregate()

    assert route.total_cost == 300.0
    assert route.total_time == 6.0
    assert pytest.approx(route.delay_prob, 0.01) == 0.2

def test_recommendation_engine():
    leg = Leg(**{"from": "A", "to": "B", "cost": 100, "time": 2, "delay_prob": 0.1, "congestion": 0.1, "geopolitical": 0.0})
    route = Route(route_id="R1", legs=[leg])
    route.aggregate()
    shipment = Shipment(shipment_id="S1", origin="A", destination="B", candidates=[route])

    result = recommend_best_route(shipment)
    assert result["shipment_id"] == "S1"
    assert result["recommended_route"]["route_id"] == "R1"