from .models import CreativeAsset


def generate_creatives(
    product_title: str,
    channel: str,
    sizes: list[str],
    count: int = 4,
) -> list[CreativeAsset]:
    if count < 1:
        raise ValueError("count must be >= 1")
    if not sizes:
        raise ValueError("sizes must not be empty")

    assets: list[CreativeAsset] = []
    for idx in range(count):
        size = sizes[idx % len(sizes)]
        asset_id = f"gen_{channel}_{idx + 1:03d}"
        assets.append(
            CreativeAsset(
                asset_id=asset_id,
                type="image",
                size=size,
                headline=f"{product_title} - 创意 {idx + 1}",
                text="AI 生成素材文案，请在发布前人工复核。",
                source="ai",
                url=f"https://cdn.example.com/{asset_id}.jpg",
            )
        )
    return assets
