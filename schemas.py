# Imports
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any


class ResumeBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    linkedin_url: Optional[str] = None
    education: Optional[Any] = None
    work_experience: Optional[Any] = None
    skills: Optional[List[str]] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    linkedin_url: Optional[str]
    education: Optional[Any]
    work_experience: Optional[Any]
    skills: Optional[List[str]]


class ResumeOut(ResumeBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
