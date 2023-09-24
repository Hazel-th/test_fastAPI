from pydantic import BaseModel
from datetime import datetime

class OperationCreate(BaseModel):
    id: int
    quantiy: str
    figi: str
    instrument_type: str
    date: datetime
    type: str