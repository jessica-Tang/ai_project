import unittest

from ad_tool.creative_generator import generate_creatives
from ad_tool.models import AdInput, Budget, CreativeAsset, Schedule, TargetingSegment
from ad_tool.planner import generate_plan_from_link
from ad_tool.structure_builder import build_account_structure


class AdToolTests(unittest.TestCase):
    def test_generate_plan_from_link(self):
        plan = generate_plan_from_link("https://shop.example.com/shoe-ultra-1", "meta", 700)
        self.assertEqual(plan.page2_defaults["channel"], "meta")
        self.assertEqual(plan.page2_defaults["budget"]["total"], 700)
        self.assertEqual(plan.product_summary.category, "鞋靴")

    def test_generate_creatives(self):
        assets = generate_creatives("跑鞋", "meta", ["1080x1080"], count=2)
        self.assertEqual(len(assets), 2)
        self.assertTrue(all(a.source == "ai" for a in assets))

    def test_build_account_structure(self):
        ad_input = AdInput(
            channel="meta",
            ad_account_id="act_demo_001",
            schedule=Schedule(start_time="2026-03-01T08:00:00+08:00", end_time="2026-03-15T23:00:00+08:00"),
            budget=Budget(currency="USD", total=300),
            targeting=[TargetingSegment(name="兴趣受众")],
            creatives=[
                CreativeAsset(
                    asset_id="img_001",
                    type="image",
                    size="1080x1080",
                    headline="标题",
                    text="文案",
                )
            ],
        )
        result = build_account_structure(ad_input)
        self.assertEqual(len(result.campaigns), 1)
        self.assertEqual(result.validation["errors"], [])
        self.assertGreaterEqual(len(result.validation["warnings"]), 1)


if __name__ == "__main__":
    unittest.main()
