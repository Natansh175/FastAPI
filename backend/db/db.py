from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
SQLALCHEMY_DATABASE_URL = (
    'mysql+pymysql://root:root@localhost:3306/fastAPI'
)

# Create engine
engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal for creating sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create a base class for models
Base = declarative_base()
