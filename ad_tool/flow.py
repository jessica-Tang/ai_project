from dataclasses import asdict
from typing import Any

from .creative_generator import generate_creatives
from .models import AdInput, Budget, CreativeAsset, Schedule, TargetingSegment
from .planner import generate_plan_from_link
from .structure_builder import build_account_structure


def run_local_flow(
    product_url: str,
    channel: str = "meta",
    budget_total: float = 500.0,
    use_ai_creatives: bool = False,
    ai_creative_count: int = 3,
) -> dict[str, Any]:
    """Run module A -> (optional C) -> B and return merged payload for local integration testing."""
    plan = generate_plan_from_link(product_url=product_url, channel_hint=channel, budget_total=budget_total)

    targeting = [
        TargetingSegment(name=item["segment"], countries=item.get("countries", ["US"]))
        for item in plan.hidden_recommendations.get("targeting", [])
    ]
    if not targeting:
        targeting = [TargetingSegment(name="兴趣受众")]

    if use_ai_creatives:
        creatives = generate_creatives(
            product_title=plan.product_summary.title,
            channel=channel,
            sizes=["1080x1080", "1080x1920"],
            count=ai_creative_count,
        )
    else:
        copy = plan.hidden_recommendations.get("copy", [])
        first_copy = copy[0] if copy else {"headline": "默认标题", "primary_text": "默认文案"}
        creatives = [
            CreativeAsset(
                asset_id="manual_001",
                type="image",
                size="1080x1080",
                headline=first_copy.get("headline", "默认标题"),
                text=first_copy.get("primary_text", "默认文案"),
                source="manual",
            )
        ]

    defaults = plan.page2_defaults
    ad_input = AdInput(
        channel=defaults["channel"],
        ad_account_id=defaults["ad_account_id"],
        schedule=Schedule(
            start_time=defaults["schedule"]["start_time"],
            end_time=defaults["schedule"]["end_time"],
        ),
        budget=Budget(
            currency=defaults["budget"]["currency"],
            total=float(defaults["budget"]["total"]),
            daily=float(defaults["budget"]["daily"]),
        ),
        targeting=targeting,
        creatives=creatives,
    )
    structure = build_account_structure(ad_input)

    return {
        "plan": plan.to_dict(),
        "creatives": [asdict(c) for c in creatives],
        "structure": structure.to_dict(),
    }
