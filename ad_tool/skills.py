from dataclasses import dataclass
from typing import Any, Protocol


class Skill(Protocol):
    name: str

    def apply(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...


@dataclass
class ChannelRecommendationSkill:
    name: str = "channel-recommendation"

    def apply(self, payload: dict[str, Any]) -> dict[str, Any]:
        defaults = payload.setdefault("page2_defaults", {})
        channel = defaults.get("channel", "meta")
        account_map = {
            "meta": "act_meta_default",
            "tiktok": "act_tiktok_default",
            "google": "act_google_default",
        }
        defaults["ad_account_id"] = account_map.get(channel, defaults.get("ad_account_id", "act_demo_001"))
        return payload


@dataclass
class ComplianceCheckSkill:
    name: str = "compliance-check"

    def apply(self, payload: dict[str, Any]) -> dict[str, Any]:
        rec = payload.setdefault("hidden_recommendations", {})
        notes = rec.setdefault("risk_notes", [])
        if "避免使用绝对化营销用语" not in notes:
            notes.append("避免使用绝对化营销用语")
        return payload


@dataclass
class BudgetAllocationSkill:
    name: str = "budget-allocation"

    def apply(self, payload: dict[str, Any]) -> dict[str, Any]:
        campaigns = payload.get("campaigns", [])
        for campaign in campaigns:
            adsets = campaign.get("adsets", [])
            if not adsets:
                continue
            total = float(campaign.get("budget", {}).get("amount", 0))
            split = round(total / len(adsets), 2) if adsets else 0
            for adset in adsets:
                budget = adset.setdefault("budget", {})
                budget["amount"] = split
                budget.setdefault("currency", campaign.get("budget", {}).get("currency", "USD"))
        return payload


def build_default_planning_skills() -> list[Skill]:
    return [ChannelRecommendationSkill(), ComplianceCheckSkill()]


def build_default_structuring_skills() -> list[Skill]:
    return [BudgetAllocationSkill(), ComplianceCheckSkill()]
