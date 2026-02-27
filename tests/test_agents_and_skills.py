import unittest

from ad_tool.agents import AccountStructuringAgent, ProjectPlanningAgent
from ad_tool.models import AdInput, Budget, CreativeAsset, Schedule, TargetingSegment


class AgentSkillTests(unittest.TestCase):
    def test_project_planning_agent_has_skill_trace(self):
        output = ProjectPlanningAgent().run(
            product_url="https://shop.example.com/shoe-ultra-1",
            channel="meta",
            budget_total=600,
        )
        self.assertEqual(output["agent"], "project-planning-agent")
        self.assertGreaterEqual(len(output["skill_trace"]), 1)
        self.assertEqual(output["result"]["page2_defaults"]["ad_account_id"], "act_meta_default")

    def test_account_structuring_agent_has_skill_trace(self):
        ad_input = AdInput(
            channel="meta",
            ad_account_id="act_demo_001",
            schedule=Schedule(start_time="2026-03-01T08:00:00+08:00", end_time="2026-03-15T23:00:00+08:00"),
            budget=Budget(currency="USD", total=300),
            targeting=[TargetingSegment(name="兴趣受众"), TargetingSegment(name="类似受众")],
            creatives=[CreativeAsset(asset_id="img_001", type="image", size="1080x1080", headline="标题", text="文案")],
        )
        output = AccountStructuringAgent().run(ad_input)
        self.assertEqual(output["agent"], "account-structuring-agent")
        self.assertIn("budget-allocation", output["skill_trace"])
        self.assertEqual(output["result"]["validation"]["errors"], [])


if __name__ == "__main__":
    unittest.main()
