#!/usr/bin/env python3
"""
Setup script to create admin user and initialize the database with test cases
"""
from app.database import SessionLocal, engine, Base
from app.models.admin import Admin
from app.models.question import Question
from app.models.test_case import TestCase
from app.routers.admin_auth import get_password_hash
from decouple import config

def setup_admin():
    """Create default admin user from environment variables"""
    db = SessionLocal()
    
    # Get credentials from environment variables
    admin_username = config("ADMIN_USERNAME", default="admin")
    admin_password = config("ADMIN_PASSWORD", default="admin123")
    
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.username == admin_username).first()
        
        if existing_admin:
            print(f"✓ Admin user '{admin_username}' already exists")
        else:
            # Create admin user
            admin = Admin(
                username=admin_username,
                password_hash=get_password_hash(admin_password)
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created successfully")
            print(f"  Username: {admin_username}")
            print(f"  Password: {admin_password}")
            print("  ⚠️  Please change the password after first login!")
        
    finally:
        db.close()

def add_sample_test_cases():
    """Add sample test cases to existing questions"""
    db = SessionLocal()
    
    try:
        # Get first question if it exists
        question = db.query(Question).first()
        
        if question:
            # Check if test cases already exist
            existing_tc = db.query(TestCase).filter(TestCase.question_id == question.id).first()
            
            if not existing_tc:
                # Add sample test cases
                test_cases = [
                    TestCase(question_id=question.id, expected_output="8", is_active=True),
                    TestCase(question_id=question.id, expected_output="30", is_active=True),
                    TestCase(question_id=question.id, expected_output="0", is_active=True),
                ]
                
                for tc in test_cases:
                    db.add(tc)
                
                db.commit()
                print(f"✓ Added {len(test_cases)} sample test cases to question: {question.title}")
            else:
                print("✓ Test cases already exist")
        else:
            print("ℹ  No questions found. Create questions through the admin panel.")
            
    finally:
        db.close()

def main():
    print("=" * 50)
    print("BroCode Admin Setup")
    print("=" * 50)
    
    # Create all tables
    print("\n1. Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Create admin user
    print("\n2. Setting up admin user...")
    setup_admin()
    
    # Add sample test cases if questions exist
    print("\n3. Checking for sample test cases...")
    add_sample_test_cases()
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Start the backend: python run.py")
    print("2. Access admin panel: http://localhost:5173/admin/login")
    print("3. Login with: admin / admin123")
    print("4. Create questions and test cases")
    print("\n⚠️  Remember to change the default admin password!")

if __name__ == "__main__":
    main()
