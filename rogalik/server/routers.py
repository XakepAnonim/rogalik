from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    """
    root
    """
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """
    read
    """
    return {"item_id": item_id, "q": q}


@router.put("/items/{item_id}")
def update_item(item_id: int, item):
    """
    put
    """
    return {"item_name": item.name, "item_id": item_id}
