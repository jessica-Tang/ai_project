from dataclasses import asdict
from typing import Any

from .creative_generator import generate_creatives
from .models import AdInput, AdPlan, AdStructure
from .planner import generate_plan_from_link
from .skills import Skill, build_default_planning_skills, build_default_structuring_skills
from .structure_builder import build_account_structure


class BaseAgent:
    def __init__(self, name: str, skills: list[Skill] | None = None) -> None:
        self.name = name
        self.skills = skills or []

    def run_skills(self, payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        applied: list[str] = []
        for skill in self.skills:
            payload = skill.apply(payload)
            applied.append(skill.name)
        return payload, applied


class ProjectPlanningAgent(BaseAgent):
    def __init__(self, skills: list[Skill] | None = None) -> None:
        super().__init__(name="project-planning-agent", skills=skills or build_default_planning_skills())

    def run(self, product_url: str, channel: str = "meta", budget_total: float = 500.0) -> dict[str, Any]:
        plan: AdPlan = generate_plan_from_link(product_url, channel, budget_total)
        payload = plan.to_dict()
        payload, skill_trace = self.run_skills(payload)
        return {"agent": self.name, "skill_trace": skill_trace, "result": payload}


class AccountStructuringAgent(BaseAgent):
    def __init__(self, skills: list[Skill] | None = None) -> None:
        super().__init__(name="account-structuring-agent", skills=skills or build_default_structuring_skills())

    def run(self, ad_input: AdInput) -> dict[str, Any]:
        structure: AdStructure = build_account_structure(ad_input)
        payload = structure.to_dict()
        payload, skill_trace = self.run_skills(payload)
        return {"agent": self.name, "skill_trace": skill_trace, "result": payload}


class CreativeGenerationAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name="creative-generation-agent", skills=[])

    def run(self, product_title: str, channel: str, sizes: list[str], count: int) -> dict[str, Any]:
        creatives = generate_creatives(product_title=product_title, channel=channel, sizes=sizes, count=count)
        return {
            "agent": self.name,
            "skill_trace": [],
            "result": [asdict(item) for item in creatives],
        }
