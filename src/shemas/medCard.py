from pydantic import BaseModel, Field

class MedCardAdd(BaseModel):
    pet_id: int
    vactination: str | None = None
    alergic: str | None = None
    chronic_diseases: str | None = None

class MedCardRequestAdd(BaseModel):
    vactination: str | None = None
    alergic: str | None = None
    chronic_diseases: str | None = None

class MedCard(MedCardAdd):
    id: int

class MedCardPatchRequest(BaseModel):
    vactination: str | None = None
    alergic: str | None = None
    chronic_diseases: str | None = None
class MedCardPatch(BaseModel):
    pet_id: int | None = None
    vactination: str | None = None
    alergic: str | None = None
    chronic_diseases: str | None = None