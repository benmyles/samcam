from pydantic import BaseModel, Field
from enum import Enum

class DogState(str, Enum):
    NONE = "none"
    SITTING = "sitting"
    STANDING = "standing"
    LYING_DOWN = "lying_down"

class DogAnalysis(BaseModel):
    is_dog: bool
    dog_state: DogState
    probability_is_panting: float = Field(ge=0.0, le=1.0)
