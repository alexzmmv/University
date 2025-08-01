"""
Migration script for Coffee Addict database using Supabase PostgreSQL

This script runs the migration process defined in database/init.py.
It will:
1. Test the connection to Supabase
2. Create tables based on models.py
3. Seed sample data if tables are empty
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Main migration function"""
    from app.database.init import run_migration
    
    # Run the migration process
    success = run_migration()
    
    if success:
        print("✅ Migration to Supabase PostgreSQL completed successfully!")
    else:
        print("❌ Migration failed. Please check the logs for details.")
        exit(1)

if __name__ == "__main__":
    main()
