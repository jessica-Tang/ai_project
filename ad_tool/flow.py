from typing import Any

from .agents import AccountStructuringAgent, CreativeGenerationAgent, ProjectPlanningAgent
from .models import AdInput, Budget, CreativeAsset, Schedule, TargetingSegment


def run_local_flow(
    product_url: str,
    channel: str = "meta",
    budget_total: float = 500.0,
    use_ai_creatives: bool = False,
    ai_creative_count: int = 3,
) -> dict[str, Any]:
    """Run agent-based flow: ProjectPlanningAgent -> (optional CreativeGenerationAgent) -> AccountStructuringAgent."""
    planning_agent = ProjectPlanningAgent()
    plan_output = planning_agent.run(product_url=product_url, channel=channel, budget_total=budget_total)
    plan = plan_output["result"]

    targeting = [
        TargetingSegment(name=item["segment"], countries=item.get("countries", ["US"]))
        for item in plan.get("hidden_recommendations", {}).get("targeting", [])
    ]
    if not targeting:
        targeting = [TargetingSegment(name="兴趣受众")]

    if use_ai_creatives:
        creative_agent = CreativeGenerationAgent()
        creative_output = creative_agent.run(
            product_title=plan["product_summary"]["title"],
            channel=channel,
            sizes=["1080x1080", "1080x1920"],
            count=ai_creative_count,
        )
        creatives = [CreativeAsset(**item) for item in creative_output["result"]]
    else:
        copy = plan.get("hidden_recommendations", {}).get("copy", [])
        first_copy = copy[0] if copy else {"headline": "默认标题", "primary_text": "默认文案"}
        creative_output = None
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

    defaults = plan["page2_defaults"]
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

    structuring_agent = AccountStructuringAgent()
    structure_output = structuring_agent.run(ad_input)

    return {
        "planning_agent": plan_output,
        "creative_agent": creative_output,
        "structuring_agent": structure_output,
    }
