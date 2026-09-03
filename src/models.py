from __future__ import annotations

from typing import List
from pydantic.v1 import BaseModel, Field, validator

class Leg(BaseModel):
    """A single leg of a shipment route."""
    from_location: str = Field(..., alias="from")
    to_location: str = Field(..., alias="to")
    cost: float
    time: float  # hours
    delay_prob: float = Field(..., ge=0.0, le=1.0)
    congestion: float = Field(..., ge=0.0, le=1.0)
    geopolitical: float = Field(..., ge=0.0, le=1.0)

    class Config:
        allow_population_by_field_name = True

    @validator("cost", "time")
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Value must be >= 0")
        return v

class Route(BaseModel):
    """A candidate route consisting of multiple legs."""
    route_id: str
    legs: List[Leg]
    total_cost: float = 0.0
    total_time: float = 0.0
    delay_prob: float = 0.0
    risk_score: float = 0.0

    def aggregate(self) -> None:
        """Populate derived fields from the legs."""
        self.total_cost = sum(l.cost for l in self.legs)
        self.total_time = sum(l.time for l in self.legs)
        self.delay_prob = sum(l.delay_prob for l in self.legs) / len(self.legs) if self.legs else 0
        avg_cong = sum(l.congestion for l in self.legs) / len(self.legs) if self.legs else 0
        avg_geo = sum(l.geopolitical for l in self.legs) / len(self.legs) if self.legs else 0
        self.risk_score = (
            0.6 * self.delay_prob + 0.2 * avg_cong + 0.2 * avg_geo
        )

class Shipment(BaseModel):
    """A shipment request with a set of candidate routes."""
    shipment_id: str
    origin: str
    destination: str
    candidates: List[Route]

    class Config:
        allow_population_by_field_name = True

    def normalise_candidates(self) -> List[dict]:
        """Return a list of dicts with normalised cost, time, and risk fields."""
        import numpy as np
        costs = np.array([c.total_cost for c in self.candidates])
        times = np.array([c.total_time for c in self.candidates])
        risks = np.array([c.risk_score for c in self.candidates])
        
        def _norm(arr):
            mn, mx = arr.min(), arr.max()
            denom = mx - mn if mx != mn else 1.0
            return (arr - mn) / denom

        norm_cost = _norm(costs)
        norm_time = _norm(times)
        norm_risk = _norm(risks)
        normalised = []
        for idx, route in enumerate(self.candidates):
            normalised.append({
                "route": route,
                "norm_cost": float(norm_cost[idx]),
                "norm_time": float(norm_time[idx]),
                "norm_risk": float(norm_risk[idx]),
            })
        return normalised