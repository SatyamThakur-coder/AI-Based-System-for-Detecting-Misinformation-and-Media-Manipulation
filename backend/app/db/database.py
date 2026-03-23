"""
Database connection and session management
Supports both SQLite (default) and PostgreSQL
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Engine configuration based on database type
connect_args = {}
engine_kwargs = {
    "pool_pre_ping": True,
}

if settings.is_sqlite:
    # SQLite needs check_same_thread=False for FastAPI
    connect_args["check_same_thread"] = False
    engine_kwargs.pop("pool_pre_ping", None)
else:
    # PostgreSQL connection pool settings
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs,
)

# Enable WAL mode for SQLite (better concurrent read performance)
if settings.is_sqlite:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
