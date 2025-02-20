from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class CustomerBase(BaseModel):
    whatsapp_number: str = Field(pattern=r'^\+?[1-9]\d{10,14}$')
    name: str = Field(..., min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    interaction_history: Optional[Dict[str, Any]] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    interaction_history: Optional[Dict[str, Any]] = None

class Customer(CustomerBase):
    id: int
    last_interaction: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True 