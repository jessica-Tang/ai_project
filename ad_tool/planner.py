from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from .models import AdPlan, Budget, ProductContext


CATEGORY_HINTS = {
    "shoe": "鞋靴",
    "dress": "服饰",
    "phone": "3C 数码",
    "bag": "箱包",
}


def _infer_category(url: str) -> str:
    url_lower = url.lower()
    for key, category in CATEGORY_HINTS.items():
        if key in url_lower:
            return category
    return "通用电商"


def _infer_title(url: str) -> str:
    parsed = urlparse(url)
    last = parsed.path.strip("/").split("/")[-1] if parsed.path else "product"
    normalized = last.replace("-", " ").replace("_", " ").strip() or "product"
    return f"{normalized.title()} 推荐商品"


def generate_plan_from_link(product_url: str, channel_hint: str = "meta", budget_total: float = 500.0) -> AdPlan:
    if not product_url.startswith(("http://", "https://")):
        raise ValueError("product_url must be a valid http(s) URL")

    now = datetime.now(timezone.utc)
    start = now + timedelta(days=1)
    end = now + timedelta(days=15)
    budget = Budget(currency="USD", total=budget_total, daily=round(budget_total / 14, 2))

    summary = ProductContext(
        product_url=product_url,
        title=_infer_title(product_url),
        highlights=["高转化卖点", "价格优势", "用户好评"],
        category=_infer_category(product_url),
    )

    page2_defaults = {
        "channel": channel_hint,
        "ad_account_id": "act_demo_001",
        "schedule": {
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        },
        "budget": {
            "currency": budget.currency,
            "daily": budget.daily,
            "total": budget.total,
        },
    }

    hidden_recommendations = {
        "targeting": [
            {"segment": "兴趣受众", "age": "18-34", "countries": ["US"]},
            {"segment": "类似受众", "age": "25-44", "countries": ["US"]},
        ],
        "copy": [
            {
                "headline": "为你挑选的人气单品",
                "primary_text": "立即查看限时优惠，点击了解更多。",
            }
        ],
        "risk_notes": ["避免使用绝对化营销用语"],
    }

    return AdPlan(
        product_summary=summary,
        page2_defaults=page2_defaults,
        hidden_recommendations=hidden_recommendations,
    )
