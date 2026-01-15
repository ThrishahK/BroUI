#!/usr/bin/env python3
"""
Database Setup Script for BroCode Challenge Platform
Supports multiple database configurations for different environments
"""

import os
import sys
from sqlalchemy import create_engine, text
from decouple import config

def setup_sqlite():
    """Setup SQLite database (default for development)"""
    print("🔧 Setting up SQLite database...")
    
    # Database URL from environment
    database_url = config("DATABASE_URL", default="sqlite:///./brocode.db")
    
    # Create engine
    engine = create_engine(database_url, echo=True)
    
    # Test connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT sqlite_version()"))
            version = result.fetchone()[0]
            print(f"✅ SQLite connected successfully (Version: {version})")
            
            # Check if tables exist
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            
            expected_tables = ['teams', 'questions', 'challenge_sessions', 'submissions']
            existing_tables = [t for t in expected_tables if t in table_names]
            
            print(f"📊 Database tables: {len(existing_tables)}/{len(expected_tables)} found")
            for table in expected_tables:
                status = "✅" if table in table_names else "❌"
                print(f"   {status} {table}")
                
    except Exception as e:
        print(f"❌ SQLite setup failed: {e}")
        return False
    
    return True

def setup_postgresql():
    """Setup PostgreSQL database"""
    print("🔧 Setting up PostgreSQL database...")
    
    database_url = config("DATABASE_URL")
    
    if "sqlite" in database_url.lower():
        print("⚠️  Current DATABASE_URL is for SQLite, not PostgreSQL")
        return False
    
    try:
        engine = create_engine(database_url, echo=True)
        
        with engine.connect() as conn:
            # Test PostgreSQL connection
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL connected successfully")
            print(f"   Version: {version.split()[1]}")
            
            # Check tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            
            expected_tables = ['teams', 'questions', 'challenge_sessions', 'submissions']
            existing_tables = [t for t in expected_tables if t in table_names]
            
            print(f"📊 Database tables: {len(existing_tables)}/{len(expected_tables)} found")
            for table in expected_tables:
                status = "✅" if table in table_names else "❌"
                print(f"   {status} {table}")
                
    except Exception as e:
        print(f"❌ PostgreSQL setup failed: {e}")
        print("💡 Make sure PostgreSQL is running and credentials are correct")
        return False
    
    return True

def main():
    print("🚀 BroCode Database Setup")
    print("=" * 50)
    
    # Load environment
    database_url = config("DATABASE_URL", default="sqlite:///./brocode.db")
    
    print(f"📍 Database URL: {database_url}")
    
    # Determine database type
    if "sqlite" in database_url.lower():
        success = setup_sqlite()
    elif "postgresql" in database_url.lower() or "postgres" in database_url.lower():
        success = setup_postgresql()
    else:
        print(f"❌ Unsupported database type in URL: {database_url}")
        print("   Supported: sqlite, postgresql")
        return
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Start the backend: python server.py")
        print("   2. Start the frontend: cd ../frontend && bun run dev")
        print("   3. Test login with: USN=TEST123, Password=testpass")
    else:
        print("\n❌ Database setup failed!")
        print("   Check your DATABASE_URL in .env file")
        sys.exit(1)

if __name__ == "__main__":
    main()
