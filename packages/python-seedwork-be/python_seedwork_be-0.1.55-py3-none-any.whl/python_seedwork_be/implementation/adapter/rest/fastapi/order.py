import json
from typing import Any, List

from dino_seedwork_be.implementation.adapter.rest.utils import to_param_orders
from dino_seedwork_be.utils.dict import extract

__all__ = ["Orders"]


class Orders:
    def __init__(self, keys: List[str]) -> None:
        self.keys = keys

    def __call__(self, orders: Any = {}) -> Any:
        match orders:
            case str():
                try:
                    orders = json.loads(orders)
                except Exception:
                    orders = {}

        plainOrders = extract(orders, self.keys)
        return to_param_orders(plainOrders)
