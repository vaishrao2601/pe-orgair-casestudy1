from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    description: str | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, ge=0)
    description: str | None = None

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None