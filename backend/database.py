# backend/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings
import logging

logger = logging.getLogger(__name__)

# Async engine dla PostgreSQL (asyncpg driver)
# Dla development: sqlite+aiosqlite:///./rekruter.db
# Dla production: postgresql+asyncpg://user:pass@host:port/db
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQL logging w dev mode
    pool_size=10,  # Connection pool
    max_overflow=20,
    pool_pre_ping=True,  # Weryfikuj connection przed użyciem
    pool_recycle=3600,  # Recykluj połączenia co godzinę
)

# Async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

# Dependency dla FastAPI endpoints
async def get_db():
    """
    FastAPI dependency - dostarcza async DB session
    Użycie: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

# Inicjalizacja tabel (tylko dla dev - w prod użyj Alembic)
async def init_db():
    """
    Tworzy wszystkie tabele w bazie (tylko development!)
    W production używaj Alembic migrations
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

# Sprawdzanie połączenia z DB
async def check_db_connection():
    """
    Health check dla database connection (ASYNC)
    """
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return {"status": "unhealthy", "database": str(e)}

