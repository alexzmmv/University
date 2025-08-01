from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    phone_number: str
    enable_2fa: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    public_id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    token_type: Optional[str] = "access"

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TwoFactorResponse(BaseModel):
    job_id: str
    message: str
    phone_number_hint: str

class TwoFactorVerificationRequest(BaseModel):
    job_id: str
    code: str

class LoginResponse(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    requires_2fa: bool = False
    job_id: Optional[str] = None
    message: Optional[str] = None
    phone_number_hint: Optional[str] = None
