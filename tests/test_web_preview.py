import unittest

from ad_tool.web_preview import _build_ad_input


class WebPreviewTests(unittest.TestCase):
    def test_build_ad_input(self):
        payload = {
            "channel": "meta",
            "ad_account_id": "act_demo_001",
            "start_time": "2026-03-01T08:00:00+08:00",
            "end_time": "2026-03-15T23:00:00+08:00",
            "budget_total": 500,
            "targeting": [{"name": "兴趣受众", "countries": ["US"]}],
            "creatives": [{"asset_id": "img_001", "headline": "标题", "text": "文案"}],
        }
        ad_input = _build_ad_input(payload)
        self.assertEqual(ad_input.channel, "meta")
        self.assertEqual(ad_input.budget.total, 500)
        self.assertEqual(len(ad_input.targeting), 1)
        self.assertEqual(len(ad_input.creatives), 1)


if __name__ == "__main__":
    unittest.main()
