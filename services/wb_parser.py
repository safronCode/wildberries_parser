import asyncio
import httpx

from entities import Product, Products, ProductSeller, ProductCard
from entities.card import get_price_per_sizes, get_options
from settings import REQUEST_HEADERS


class WBParser:
    SEARCH_URL = r"https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search"

    def __init__(self):
        self.headers = REQUEST_HEADERS
        self.timeout = httpx.Timeout(20)
        self.limits = httpx.Limits(
            max_connections=10,
            max_keepalive_connections=15,
        )
        self.concurrent_requests = 5

    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
            limits=self.limits,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _get(self, url: str, params: dict = None) -> dict:
        response = await self.client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    async def fetch_products(self, params) -> Products:
        data: dict = await self._get(url=self.SEARCH_URL, params=params)
        products = data.get("products", dict())

        return Products([
            Product(
                article=p["id"],
                pics_cnt=p.get("pics", 0),

                card = ProductCard(
                    name = p.get("name", ""),
                    review_rating = float(p.get("reviewRating", 0)),
                    nm_feedbacks = int(p.get("nmFeedbacks", 0)),
                    total_quantity= int(p.get("totalQuantity", 0)),
                    price_per_size = get_price_per_sizes(p.get("sizes", [])),
                ),

                seller = ProductSeller(
                    id=p.get("supplierId"),
                    name=p.get("supplier"),
                ),

            )
            for p in products if p.get("id")
        ])

    async def _fetch_one_detail(self, semaphore, product: Product):

        async with (semaphore):
            try:
                card = product.card
                data = await self._get(url=product.get_card_url)
                card.description = data.get("description", "")
                card.options = get_options(data.get("options"))

                return product

            except Exception as e:
                print(e)
                return None

    async def fetch_products_detail(self, semaphore, products: Products) -> Products:
        tasks = [ self._fetch_one_detail(semaphore, product) for product in products ]
        result = await asyncio.gather(*tasks)
        return Products([p for p in result if p is not None])

    async def _parse_one_page(self, semaphore, base_params: dict, page: int) -> Products:
        async with semaphore:
            params = base_params.copy()
            params["page"] = page
            return await self.fetch_products(params)

    async def parse(self, params: dict, pages: range) -> Products:
        async with (self):
            semaphore = asyncio.Semaphore(self.concurrent_requests)

            tasks = [
                self._parse_one_page(semaphore, params, page)
                for page in pages
            ]
            parsed_pages = await asyncio.gather(*tasks)

            all_products = Products()
            for parsed_page in parsed_pages:
                all_products.extend(parsed_page)

            all_products_extended: Products = await self.fetch_products_detail(semaphore, all_products)
            return all_products_extended
