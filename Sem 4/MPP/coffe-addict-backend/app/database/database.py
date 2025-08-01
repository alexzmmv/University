from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import socket
import sys

# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Use environment variables to determine which database to use
USE_SQLITE = os.environ.get("USE_SQLITE", "false").lower() == "true"
USE_SUPABASE = os.environ.get("USE_SUPABASE", "true").lower() == "true"

if USE_SQLITE:
    print("Using SQLite for development (not recommended for migrations)")
else:
    print("Using Supabase PostgreSQL for development and migrations")

# If DATABASE_URL is not set, construct it from individual parameters
if not DATABASE_URL:
    print("DATABASE_URL not found, attempting to construct from individual parameters...")
    try:
        # Try relative import first
        from .init import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
    except (ImportError, ValueError):
        # Fallback to environment variables
        DB_NAME = os.environ.get("SUPABASE_DB_NAME", "postgres")
        DB_USER = os.environ.get("SUPABASE_DB_USER", "postgres")
        DB_PASSWORD = os.environ.get("SUPABASE_DB_PASSWORD", "your-password") 
        DB_HOST = os.environ.get("SUPABASE_DB_HOST", "db.abcdefghijklm.supabase.co")
        DB_PORT = os.environ.get("SUPABASE_DB_PORT", "5432")
    
    # Construct database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
    print(f"Constructed DATABASE_URL from individual parameters")

# Ensure DATABASE_URL starts with postgresql:// if needed
if "postgres" in DATABASE_URL and "@" in DATABASE_URL and not DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = "postgresql://" + DATABASE_URL

try:
    # Extract hostname from DATABASE_URL
    # Format is typically: postgresql://user:password@hostname:port/dbname
    hostname_part = DATABASE_URL.split("@")[1].split("/")[0]
    hostname = hostname_part.split(":")[0]
    
    print(f"Database hostname: {hostname}")
    
    # Try to resolve the hostname
    try:
        host_info = socket.getaddrinfo(hostname, 0)
        print(f"Successfully resolved database hostname")
    except socket.gaierror as e:
        print(f"Warning: Could not resolve database hostname: {e}")
        print("Continuing with unresolved hostname; this may cause connection issues")
except Exception as e:
    print(f"Error parsing DATABASE_URL: {e}")

# Create SQLAlchemy engine with options to handle connection issues
engine = create_engine(
    DATABASE_URL,
    connect_args={
        # Set connection timeout
        "connect_timeout": 30,
        # Allow both IPv4 and IPv6
        "gssencmode": "disable", 
        "target_session_attrs": "any"
    },
    pool_pre_ping=True,  # Verify connection is still alive
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=5,         # Connection pool size
    max_overflow=10,     # Allow up to 10 connections beyond pool_size
    echo=True            # Log SQL queries for debugging
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()