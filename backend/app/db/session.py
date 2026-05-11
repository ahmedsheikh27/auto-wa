from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from app.core.config import Settings

DATABASE_URI = 'postgresql://postgres.wzqcnxlhxfxucochrumk:GdimT20uoHs8W3Ln@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres'

engine = create_engine(DATABASE_URI)    
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
print('Database connected successfully')

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()