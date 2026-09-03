import json
import argparse
from src.models import Shipment
from src.engine import recommend_best_route

def main():
    parser = argparse.ArgumentParser(description="Safiri AI Shipment Route Optimizer")
    parser.add_argument("--input", required=True, help="Path to input JSON dataset file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        raw_data = json.load(f)

    shipments = [Shipment.parse_obj(data) for data in raw_data]

    # Pre-calculate totals for each route
    for shipment in shipments:
        for candidate in shipment.candidates:
            candidate.aggregate()

    print(f"\nSuccessfully loaded {len(shipments)} shipments. Processing optimal routes...\n")
    print("-" * 60)

    for idx, shipment in enumerate(shipments[:5], 1):
        result = recommend_best_route(shipment)
        best = result["recommended_route"]
        print(f"[{idx}] Shipment ID: {shipment.shipment_id}")
        print(f"    Recommended Route: {best['route_id']}")
        print(f"    Total Cost:        ${best['total_cost']}")
        print(f"    Total Time:        {best['total_time']} hours")
        print(f"    Composite Score:   {best['score']}")
        print(f"    Details:           {result['explanation']}\n")

if __name__ == "__main__":
    main()