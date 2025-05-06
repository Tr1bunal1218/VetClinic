from pydantic import BaseModel, Field


class PetRequestAdd(BaseModel):
    breed: str | None = Field(None)
    name: str
    age: int | None = Field(None)
    sex: str | None = Field(None)
    vid: str | None = Field(None)
    ...#че нить еще

class PetAdd(PetRequestAdd):
    user_id: int
    
class Pet(PetAdd):
    id: int
