from pydantic import BaseModel
from typing import List, Dict

class Device(BaseModel):
    device_id: str
    name: str
    description: str | None = None
    type: str
    is_active: bool
    actions: List[str] = []
    sensors: List[str] = []
