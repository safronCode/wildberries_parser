from dataclasses import dataclass

@dataclass(slots=True)
class ProductSeller:
    id: int
    name: str

    @property
    def get_seller_url(self) -> str:
        return f"https://www.wildberries.ru/seller/{self.id}"
