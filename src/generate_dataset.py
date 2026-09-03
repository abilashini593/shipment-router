import json, random, uuid, os
from pathlib import Path
from src.models import Leg, Route, Shipment

def rand_range(lo: float, hi: float) -> float:
    return round(random.uniform(lo, hi), 2)

def make_leg() -> dict:
    locations = ["NYC", "LON", "HKG", "DXB", "SIN"]
    frm = random.choice(locations)
    to = random.choice([l for l in locations if l != frm])
    return {
        "from": frm,
        "to": to,
        "cost": rand_range(100, 2000),
        "time": rand_range(10, 240),
        "delay_prob": rand_range(0.01, 0.30),
        "congestion": rand_range(0, 0.5),
        "geopolitical": rand_range(0, 0.5),
    }

def make_route() -> Route:
    leg_count = random.randint(2, 4)
    legs = [Leg(**make_leg()) for _ in range(leg_count)]
    route = Route(route_id=str(uuid.uuid4()), legs=legs)
    route.aggregate()
    return route

def make_shipment() -> Shipment:
    candidate_count = random.randint(3, 5)
    candidates = [make_route() for _ in range(candidate_count)]
    return Shipment(
        shipment_id=str(uuid.uuid4()),
        origin="NYC",
        destination="LON",
        candidates=candidates,
    )

def generate_dataset(num_shipments: int = random.randint(20, 50)) -> None:
    data = [make_shipment().dict() for _ in range(num_shipments)]
    out_dir = Path(__file__).resolve().parents[1] / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "shipment_dataset.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {num_shipments} shipments to {out_file}")

if __name__ == "__main__":
    generate_dataset()
