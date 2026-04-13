from dataclasses import dataclass, field

from utils import get_cdn_url
from entities import ProductCard, ProductSeller


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
    def get_pics_urls_str(self) -> str:
        return ",\n".join([ self.cdn_url + fr"images/big/{i + 1}.webp" for i in range(0, self.pics_cnt)])

    @property
    def get_card_url(self) -> str:
        return self.cdn_url + "info/ru/card.json"

    def to_dict(self) -> dict:
        return {
            "article": self.article,
            "product_url": self.get_product_url,
            "name": self.card.name,
            "description": self.card.description,
            "pics_url": self.get_pics_urls_str,
            "options": self.card.options_str,
            "seller": self.seller.name,
            "seller_url": self.seller.get_seller_url,
            "price_per_size": self.card.price_per_size_str,
            "total_quantity": self.card.total_quantity,
            "rating": self.card.review_rating,
            "nm_feedbacks": self.card.nm_feedbacks,
        }


@dataclass
class Products:
    items: list[Product] = field(default_factory=list)

    def __iter__(self):
        return iter(self.items)

    def __add__(self, other: "Products"):
        if not isinstance(other, Products):
            return NotImplemented
        return Products(self.items + other.items)

    def extend(self, iterable):
        self.items.extend(iterable)
