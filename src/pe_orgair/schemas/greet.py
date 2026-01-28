from pydantic import BaseModel, Field

class GreetUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=120)