from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from constants import DATABASE_CREDENTIALS

DATABASE_URL = (
    f"postgresql+asyncpg://{DATABASE_CREDENTIALS['user']}:"
    f"{DATABASE_CREDENTIALS['password']}@{DATABASE_CREDENTIALS['host']}:"
    f"{DATABASE_CREDENTIALS['port']}/{DATABASE_CREDENTIALS['database']}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
