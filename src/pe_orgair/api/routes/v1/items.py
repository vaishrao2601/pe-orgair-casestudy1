from fastapi import APIRouter, HTTPException
from pe_orgair.schemas.items import ItemCreate, ItemUpdate, ItemOut

router = APIRouter(prefix="/items", tags=["Items"])

# fake in-memory DB for lab
_DB: dict[int, ItemOut] = {}
_NEXT_ID = 1

@router.post("", response_model=ItemOut)
def create_item(payload: ItemCreate):
    global _NEXT_ID
    item = ItemOut(id=_NEXT_ID, **payload.model_dump())
    _DB[_NEXT_ID] = item
    _NEXT_ID += 1
    return item

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    if item_id not in _DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return _DB[item_id]

@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate):
    if item_id not in _DB:
        raise HTTPException(status_code=404, detail="Item not found")

    current = _DB[item_id].model_dump()
    updates = payload.model_dump(exclude_unset=True)

    updated = ItemOut(**{**current, **updates})
    _DB[item_id] = updated
    return updated

@router.delete("/{item_id}")
def delete_item(item_id: int):
    if item_id not in _DB:
        raise HTTPException(status_code=404, detail="Item not found")
    del _DB[item_id]
    return {"deleted": item_id}