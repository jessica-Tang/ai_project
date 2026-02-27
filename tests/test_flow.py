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
        self.assertIn("plan", payload)
        self.assertIn("creatives", payload)
        self.assertIn("structure", payload)
        self.assertEqual(len(payload["creatives"]), 2)
        self.assertEqual(payload["structure"]["validation"]["errors"], [])


if __name__ == "__main__":
    unittest.main()
