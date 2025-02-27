# Imports
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Resume
from schemas import ResumeCreate, ResumeUpdate


async def get_resume(db: AsyncSession, resume_id):
    result = await db.execute(select(Resume).filter(Resume.id == resume_id))
    return result.scalar_one_or_none()


async def get_resumes(db: AsyncSession, skip: int = 0, limit=100, skill=None):
    query = select(Resume)
    if skill:
        # Case-insensitive search
        query = query.filter(text(":skill ILIKE ANY (resumes.skills)")).params(skill=skill)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_resume(db: AsyncSession, resume: ResumeCreate):
    db_resume = Resume(**resume.dict())
    db.add(db_resume)
    await db.commit()
    await db.refresh(db_resume)
    return db_resume


async def update_resume(db: AsyncSession, resume_id, resume: ResumeUpdate):
    db_resume = await get_resume(db, resume_id)
    if db_resume is None:
        return None
    for key, value in resume.dict(exclude_unset=True).items():
        setattr(db_resume, key, value)
    await db.commit()
    await db.refresh(db_resume)
    return db_resume


async def delete_resume(db: AsyncSession, resume_id):
    db_resume = await get_resume(db, resume_id)
    if db_resume is None:
        return False
    await db.delete(db_resume)
    await db.commit()
    return True
