import asyncio

from entities import Products
from utils import get_parsed_data

def _write_file():
    ...

def start_parsing():
    query = input("Enter you query: ")
    parsed_data: Products = asyncio.run(get_parsed_data(query))

    data_to_write: list[dict] = [d.to_dict() for d in parsed_data]

    _write_file()


