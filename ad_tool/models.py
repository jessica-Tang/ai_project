from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Budget:
    currency: str = "USD"
    total: float = 500.0
    daily: float | None = None


@dataclass
class Schedule:
    start_time: str
    end_time: str


@dataclass
class TargetingSegment:
    name: str
    countries: list[str] = field(default_factory=lambda: ["US"])
    age_min: int = 18
    age_max: int = 34


@dataclass
class CreativeAsset:
    asset_id: str
    type: str
    size: str
    headline: str
    text: str
    source: str = "manual"
    url: str | None = None


@dataclass
class ProductContext:
    product_url: str
    title: str
    highlights: list[str]
    category: str


@dataclass
class AdPlan:
    product_summary: ProductContext
    page2_defaults: dict[str, Any]
    hidden_recommendations: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["product_summary"] = asdict(self.product_summary)
        return payload


@dataclass
class AdInput:
    channel: str
    ad_account_id: str
    schedule: Schedule
    budget: Budget
    targeting: list[TargetingSegment]
    creatives: list[CreativeAsset]


@dataclass
class AdStructure:
    campaigns: list[dict[str, Any]]
    validation: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
