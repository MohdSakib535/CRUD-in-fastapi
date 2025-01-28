from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""
Components of the URL
sqlite://:

Specifies the database driver to use.
sqlite is the database type, and the sqlite:// prefix indicates that the app will use SQLite.
/:

The first / is part of the URL syntax.
./test.db:

The path to the SQLite database file.
./: Refers to the current directory where the application is running.
blog.db: The name of the SQLite database file.
If this file doesn't exist, SQLite will automatically create it when the first connection is made.
"""
# SQLite database URL
DATABASE_URL = "postgresql://admin:admin@localhost:5432/fastapi-crud"

# Create database engine
engine = create_engine(DATABASE_URL)



# # Create a SessionLocal class for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

"""
SessionLocal() creates a new session.
The yield keyword allows the session to be used within the request.
db.close() ensures the session is properly closed after the request is processed.

"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()