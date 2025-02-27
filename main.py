# Imports
from typing import List
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import schemas, operations
from database import async_session, engine, Base
from auth import get_current_user, authenticate_user, create_access_token

app = FastAPI(title="Resume API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_db():
    async with async_session() as session:
        yield session


@app.get("/resumes", response_model=List[schemas.ResumeOut])
async def list_resumes(
        skip: int = 0, limit: int = 100, skill: str = None,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    resumes = await operations.get_resumes(db, skip=skip, limit=limit,
                                           skill=skill)
    return resumes


@app.get("/resumes/{resume_id}", response_model=schemas.ResumeOut)
async def get_resume(
        resume_id: int,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    db_resume = await operations.get_resume(db, resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume


@app.post("/resumes", response_model=schemas.ResumeOut, status_code=202)
async def create_resume(
        resume: schemas.ResumeCreate,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return await operations.create_resume(db, resume)


@app.put("/resumes/{resume_id}", response_model=schemas.ResumeOut)
async def update_resume(
        resume_id: int, resume: schemas.ResumeUpdate,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    db_resume = await operations.update_resume(db, resume_id, resume)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume


@app.delete("/resumes/{resume_id}", status_code=204)
async def delete_resume(
        resume_id: int,
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    success = await operations.delete_resume(db, resume_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resume not found")
    return None
