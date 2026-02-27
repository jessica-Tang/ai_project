import argparse
import json

from .creative_generator import generate_creatives
from .models import AdInput, Budget, CreativeAsset, Schedule, TargetingSegment
from .planner import generate_plan_from_link
from .structure_builder import build_account_structure


def _json_default(obj):
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def cmd_plan(args: argparse.Namespace) -> None:
    plan = generate_plan_from_link(args.product_url, args.channel, args.budget)
    print(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2, default=_json_default))


def cmd_creative(args: argparse.Namespace) -> None:
    sizes = [s.strip() for s in args.sizes.split(",") if s.strip()]
    assets = generate_creatives(args.product_title, args.channel, sizes, args.count)
    print(json.dumps([a.__dict__ for a in assets], ensure_ascii=False, indent=2))


def cmd_structure(args: argparse.Namespace) -> None:
    creatives: list[CreativeAsset] = []
    for index in range(args.creative_count):
        creatives.append(
            CreativeAsset(
                asset_id=f"manual_{index + 1:03d}",
                type="image",
                size="1080x1080",
                headline=f"手动素材 {index + 1}",
                text="用户上传素材",
            )
        )

    targeting = [TargetingSegment(name=n.strip()) for n in args.targeting.split(",") if n.strip()]
    ad_input = AdInput(
        channel=args.channel,
        ad_account_id=args.account,
        schedule=Schedule(start_time=args.start, end_time=args.end),
        budget=Budget(currency=args.currency, total=args.budget),
        targeting=targeting,
        creatives=creatives,
    )
    structure = build_account_structure(ad_input)
    print(json.dumps(structure.to_dict(), ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI 广告生成工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan", help="模块A：根据产品链接生成投放草案")
    p_plan.add_argument("product_url")
    p_plan.add_argument("--channel", default="meta")
    p_plan.add_argument("--budget", type=float, default=500.0)
    p_plan.set_defaults(func=cmd_plan)

    p_creative = sub.add_parser("creative", help="模块C：生成素材")
    p_creative.add_argument("product_title")
    p_creative.add_argument("--channel", default="meta")
    p_creative.add_argument("--sizes", default="1080x1080,1080x1920")
    p_creative.add_argument("--count", type=int, default=4)
    p_creative.set_defaults(func=cmd_creative)

    p_structure = sub.add_parser("structure", help="模块B：生成账户结构")
    p_structure.add_argument("--channel", default="meta")
    p_structure.add_argument("--account", default="act_demo_001")
    p_structure.add_argument("--start", default="2026-03-01T08:00:00+08:00")
    p_structure.add_argument("--end", default="2026-03-15T23:00:00+08:00")
    p_structure.add_argument("--currency", default="USD")
    p_structure.add_argument("--budget", type=float, default=500.0)
    p_structure.add_argument("--targeting", default="兴趣受众,类似受众")
    p_structure.add_argument("--creative-count", type=int, default=2)
    p_structure.set_defaults(func=cmd_structure)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
