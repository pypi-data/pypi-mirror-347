from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoTokenSchemas:
    class Token(BaseModel):
        token:str = Field(..., description="Token")