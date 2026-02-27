import unittest

from ad_tool.flow import run_local_flow


class FlowTests(unittest.TestCase):
    def test_run_local_flow_with_ai_creatives(self):
        payload = run_local_flow(
            product_url="https://shop.example.com/shoe-ultra-1",
            channel="meta",
            budget_total=650,
            use_ai_creatives=True,
            ai_creative_count=2,
        )
        self.assertIn("planning_agent", payload)
        self.assertIn("structuring_agent", payload)
        self.assertIn("creative_agent", payload)
        self.assertEqual(payload["planning_agent"]["agent"], "project-planning-agent")
        self.assertEqual(payload["structuring_agent"]["result"]["validation"]["errors"], [])


if __name__ == "__main__":
    unittest.main()
