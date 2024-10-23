from pydantic import BaseModel


class Item(BaseModel):
    """
    item fdsgdsg
    """

    name: str
    price: float
    is_offer: bool | None = None
