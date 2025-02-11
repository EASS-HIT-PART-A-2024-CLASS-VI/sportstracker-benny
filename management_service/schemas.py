# management_service/schemas.py
from pydantic import BaseModel

class TeamCreate(BaseModel):
    name: str
    city: str

class TeamResponse(BaseModel):
    id: int
    name: str
    city: str

    class Config:
        orm_mode = True
