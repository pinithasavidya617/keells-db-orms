from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):

    name: str = Field(..., min_length=3, max_length=255)
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[str] = None

class UserResponse(UserBase):

    id: int

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    user_id : int
    amount: float
    description: str
    created_at: datetime

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    amount: float
    description: str
    created_at: datetime

class InvoiceResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True