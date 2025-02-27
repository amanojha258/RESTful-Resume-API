# Imports
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    linkedin_url = Column(String, nullable=True)
    education = Column(JSON, nullable=True)
    work_experience = Column(JSON, nullable=True)
    skills = Column(ARRAY(String), nullable=True)
