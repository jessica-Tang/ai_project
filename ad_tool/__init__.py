"""AI ad generation toolkit prototype."""

from .agents import AccountStructuringAgent, CreativeGenerationAgent, ProjectPlanningAgent
from .flow import run_local_flow
from .models import (
    AdInput,
    AdPlan,
    AdStructure,
    Budget,
    CreativeAsset,
    ProductContext,
    Schedule,
    TargetingSegment,
)
from .planner import generate_plan_from_link
from .skills import (
    BudgetAllocationSkill,
    ChannelRecommendationSkill,
    ComplianceCheckSkill,
    build_default_planning_skills,
    build_default_structuring_skills,
)
from .structure_builder import build_account_structure
from .creative_generator import generate_creatives
from .web_preview import run_preview_server

__all__ = [
    "AdInput",
    "AdPlan",
    "AdStructure",
    "Budget",
    "CreativeAsset",
    "ProductContext",
    "Schedule",
    "TargetingSegment",
    "generate_plan_from_link",
    "build_account_structure",
    "generate_creatives",
    "run_local_flow",
    "ProjectPlanningAgent",
    "AccountStructuringAgent",
    "CreativeGenerationAgent",
    "ChannelRecommendationSkill",
    "ComplianceCheckSkill",
    "BudgetAllocationSkill",
    "build_default_planning_skills",
    "build_default_structuring_skills",
    "run_preview_server",
]
