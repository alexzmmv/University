import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Supabase database connection parameters
DB_NAME = os.environ.get("SUPABASE_DB_NAME", "postgres")
DB_USER = os.environ.get("SUPABASE_DB_USER", "postgres")
DB_PASSWORD = os.environ.get("SUPABASE_DB_PASSWORD", "your-password")
DB_HOST = os.environ.get("SUPABASE_DB_HOST", "db.abcdefghijklm.supabase.co")
DB_PORT = os.environ.get("SUPABASE_DB_PORT", "5432")

def connect_database():
    """Test connection to the database"""
    try:
        print(f"Connecting to Supabase: {DB_HOST}")
        # Connect to PostgreSQL on Supabase
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode='require'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to Supabase PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

def create_tables():
    """Create tables in Supabase PostgreSQL if they don't exist"""
    # Import here to avoid circular imports
    from .database import engine
    from .models.models import Base
    
    print("Creating tables in Supabase PostgreSQL...")
    try:
        # Create all tables defined in models
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def alter_tables():
    """Alter existing tables to add new columns"""
    from .database import engine
    import sqlalchemy as sa
    
    print("Altering tables to add new columns...")
    try:
        # Create a connection
        conn = engine.connect()
        
        # Check if phone_number column exists in users table
        inspector = sa.inspect(engine)
        user_columns = [column['name'] for column in inspector.get_columns('users')]
        
        if 'phone_number' not in user_columns:
            print("Adding phone_number column to users table...")
            conn.execute(sa.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR"))
            conn.commit()
            print("Column added successfully!")
        else:
            print("phone_number column already exists.")
            
        # Check if enable_2fa column exists in users table
        if 'enable_2fa' not in user_columns:
            print("Adding enable_2fa column to users table...")
            conn.execute(sa.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS enable_2fa BOOLEAN DEFAULT FALSE"))
            conn.commit()
            print("enable_2fa column added successfully!")
        else:
            print("enable_2fa column already exists.")
        
        conn.close()
        return True
    except Exception as e:
        print(f"Error altering tables: {e}")
        return False

def seed_sample_data():
    """Seed sample data into tables if they are empty"""
    try:
        # Import here to avoid circular imports
        from .database import SessionLocal
        from .models.models import CoffeeShop, Drink, User
        import uuid
        import random
        import sys
        import os
        
        # Add the app directory to the path for imports
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from auth.password import get_password_hash
        
        db = SessionLocal()
        
        # Check if users table is empty
        if db.query(User).count() == 0:
            print("Seeding sample user...")
            
            # Create a sample user
            sample_user = User(
                public_id=str(uuid.uuid4()),
                email="user@example.com",
                username="testuser",
                hashed_password=get_password_hash("password123"),
                phone_number="1234567890",
                enable_2fa=False,
                is_active=True
            )
            db.add(sample_user)
            db.commit()
            print("Sample user added! Username: testuser, Password: password123")
        
        # Check if coffee_shops table is empty
        if db.query(CoffeeShop).count() == 0:
            print("Seeding sample coffee shops...")
            
            # Sample coffee shop data
            sample_shops = [
                {
                    "name": "Coffee Haven",
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "rating": 4.5,
                    "status": "Open Now",
                    "image": "https://images.unsplash.com/photo-1559305616-3f99cd43e353"
                },
                {
                    "name": "Espresso Express",
                    "latitude": 37.7833,
                    "longitude": -122.4167,
                    "rating": 4.2,
                    "status": "Open Now",
                    "image": "https://images.unsplash.com/photo-1559925393-8be0ec4767c8"
                },
                {
                    "name": "Brew & Bean",
                    "latitude": 37.7694,
                    "longitude": -122.4862,
                    "rating": 4.8,
                    "status": "Closed",
                    "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3"
                }
            ]
            
            # Add coffee shops
            for shop_data in sample_shops:
                shop = CoffeeShop(
                    public_id=str(uuid.uuid4()),
                    name=shop_data["name"],
                    latitude=shop_data["latitude"],
                    longitude=shop_data["longitude"],
                    rating=shop_data["rating"],
                    status=shop_data["status"],
                    image=shop_data["image"]
                )
                db.add(shop)
            
            db.commit()
            print("Sample coffee shops added!")
            
            # Add drinks for each coffee shop
            print("Seeding sample drinks...")
            shops = db.query(CoffeeShop).all()
            
            drink_templates = [
                {"name": "Espresso", "price": "3.50", "popularity": 85},
                {"name": "Cappuccino", "price": "4.50", "popularity": 90},
                {"name": "Latte", "price": "4.75", "popularity": 95},
                {"name": "Americano", "price": "3.75", "popularity": 80},
                {"name": "Mocha", "price": "5.25", "popularity": 88}
            ]
            
            for shop in shops:
                for drink in drink_templates:
                    sales = random.randint(50, 200)
                    db.add(Drink(
                        name=drink["name"],
                        description=f"A delicious {drink['name'].lower()} made with premium beans",
                        price=drink["price"],
                        image=f"https://source.unsplash.com/random/300x200?{drink['name'].lower()}",
                        sales=sales,
                        popularity=drink["popularity"],
                        coffee_shop_id=shop.id
                    ))
            
            db.commit()
            print("Sample drinks added!")
        else:
            print("Database already contains data, skipping seed")
        
        db.close()
        return True
    except Exception as e:
        print(f"Error seeding data: {e}")
        return False

def run_migration():
    """Run the complete migration process"""
    print("Starting database migration process...")
    
    # Step 1: Test connection
    if not connect_database():
        print("Connection failed, aborting migration")
        return False
    
    # Step 2: Create tables
    if not create_tables():
        print("Table creation failed, aborting migration")
        return False
    
    # Step 3: Alter tables
    if not alter_tables():
        print("Table alteration failed, aborting migration")
        return False
    
    # Step 4: Seed data (optional)
    seed_sample_data()
    
    print("Migration completed successfully!")
    return True

if __name__ == "__main__":
    run_migration()