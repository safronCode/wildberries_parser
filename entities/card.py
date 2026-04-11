from dataclasses import dataclass, field

def get_price_per_sizes(sizes: list[dict]) -> dict[str, int]:
    price_size_map = dict()
    for size in sizes:
        if (current_size := size.get("name")) and (current_price := size.get("price", {}).get("basic", 0)):
            price_size_map[current_size] = current_price // 100

    return price_size_map

def get_options(options: list[dict]) -> dict[str, str]:
    return {option["name"]: option["value"] for option in options if options}


@dataclass(slots=True)
class ProductCard:
    name: str
    review_rating: float
    nm_feedbacks: int
    total_quantity: int
    price_per_size: dict[str, int]

    description: str = ""
    options: dict[str, str] = field(default_factory=dict)
