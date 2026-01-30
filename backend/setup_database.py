#!/usr/bin/env python3
"""
Database Setup Script for BroCode Challenge Platform
Supports multiple database configurations for different environments
"""

import os
import sys
import hashlib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from decouple import config

# Import models and database setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.database import Base
from app.models import Team, Question, ChallengeSession, Submission

def setup_sqlite():
    """Setup SQLite database (default for development)"""
    print("🔧 Setting up SQLite database...")
    
    # Database URL from environment
    database_url = config("DATABASE_URL", default="sqlite:///./brocode.db")
    
    # Create engine
    engine = create_engine(database_url, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Test connection and create tables
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT sqlite_version()"))
            version = result.fetchone()[0]
            print(f"✅ SQLite connected successfully (Version: {version})")
        
        # Create all tables
        print("📦 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
        
        # Check if tables exist
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            
            expected_tables = ['teams', 'questions', 'challenge_sessions', 'submissions']
            existing_tables = [t for t in expected_tables if t in table_names]
            
            print(f"📊 Database tables: {len(existing_tables)}/{len(expected_tables)} found")
            for table in expected_tables:
                status = "✅" if table in table_names else "❌"
                print(f"   {status} {table}")
        
        # Create test teams if they don't exist
        print("\n👥 Creating test teams...")
        db = SessionLocal()
        try:
            # Test team 1: TEST123 / testpass
            team1 = db.query(Team).filter(Team.team_leader_usn == "TEST123").first()
            if not team1:
                # Use SHA256 hash for testpass (as per auth.py fallback)
                password_hash = hashlib.sha256("testpass".encode()).hexdigest()
                team1 = Team(
                    team_leader_usn="TEST123",
                    password=password_hash,
                    team_name="Test Team"
                )
                db.add(team1)
                print("   ✅ Created team: TEST123 / testpass")
            else:
                print("   ℹ️  Team TEST123 already exists")
            
            # Test team 2: NNM24AC008 / NNM24AC008
            team2 = db.query(Team).filter(Team.team_leader_usn == "NNM24AC008").first()
            if not team2:
                # Use SHA256 hash for NNM24AC008
                password_hash = hashlib.sha256("NNM24AC008".encode()).hexdigest()
                team2 = Team(
                    team_leader_usn="NNM24AC008",
                    password=password_hash,
                    team_name="Team NNM24AC008"
                )
                db.add(team2)
                print("   ✅ Created team: NNM24AC008 / NNM24AC008")
            else:
                print("   ℹ️  Team NNM24AC008 already exists")
            
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"   ⚠️  Error creating teams: {e}")
        finally:
            db.close()
                
    except Exception as e:
        print(f"❌ SQLite setup failed: {e}")
        import traceback
        traceback.print_exc()
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
