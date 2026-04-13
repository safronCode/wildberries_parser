from math import ceil

from utils import get_toml_tables
from entities import Products
from services import WBParser


async def get_parsed_data(query: str = None) -> Products:
    config: dict = get_toml_tables(["payload", "io-settings"])
    payload: dict = config["payload"]
    if query:
        payload["query"] = input("Enter your query: ").strip()
    page_range: range = range(1, ceil(config["io-settings"]["max_records_value"] / 100))

    async with WBParser() as parser:
        products = await parser.parse(payload, page_range)

    return products
