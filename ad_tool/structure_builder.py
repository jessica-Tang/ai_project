from dataclasses import asdict

from .models import AdInput, AdStructure


def build_account_structure(ad_input: AdInput) -> AdStructure:
    errors: list[str] = []
    warnings: list[str] = []

    if ad_input.budget.total <= 0:
        errors.append("budget.total must be > 0")
    if not ad_input.targeting:
        errors.append("at least one targeting segment is required")
    if not ad_input.creatives:
        errors.append("at least one creative is required")
    if len(ad_input.targeting) == 1:
        warnings.append("当前仅 1 个受众包，建议进行 A/B 测试")

    split_budget = round(ad_input.budget.total / max(len(ad_input.targeting), 1), 2)
    adsets = []
    for segment in ad_input.targeting:
        ads = [
            {
                "name": f"AD_{creative.asset_id}",
                "creative_ref": creative.asset_id,
                "headline": creative.headline,
                "text": creative.text,
            }
            for creative in ad_input.creatives
        ]

        adsets.append(
            {
                "name": f"ADSET_{segment.name}",
                "budget": {"currency": ad_input.budget.currency, "amount": split_budget},
                "targeting": asdict(segment),
                "ads": ads,
            }
        )

    campaigns = [
        {
            "name": "CAMP_AUTO_GEN_001",
            "objective": "CONVERSIONS",
            "budget": {
                "currency": ad_input.budget.currency,
                "amount": ad_input.budget.total,
            },
            "schedule": asdict(ad_input.schedule),
            "channel": ad_input.channel,
            "ad_account_id": ad_input.ad_account_id,
            "adsets": adsets,
        }
    ]

    return AdStructure(campaigns=campaigns, validation={"errors": errors, "warnings": warnings})
