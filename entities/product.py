from dataclasses import dataclass, field

from entities import ProductCard, ProductSeller
from utils.get_cdn_url import get_cdn_url


@dataclass(slots=True)
class Product:
    article: int

    card: ProductCard
    seller: ProductSeller

    pics_cnt: int
    cdn_url: str = ""

    def __post_init__(self):
        self.cdn_url: str = get_cdn_url(self.article)

    @property
    def get_product_url(self) -> str:
        return f"https://www.wildberries.ru/catalog/{self.article}/detail.aspx"

    @property
    def get_pics_urls(self) -> list[str]:
        return [ self.cdn_url + fr"images/big/{i + 1}.webp" for i in range(0, self.pics_cnt)]

    @property
    def get_card_url(self) -> str:
        return self.cdn_url + "info/ru/card.json"

@dataclass
class Products:
    items: list[Product] = field(default_factory=list)

    def __iter__(self):
        return iter(self.items)

    def __add__(self, other: "Products"):
        if not isinstance(other, Products):
            return NotImplemented
        return Products(self.items + other.items)
