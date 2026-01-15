#!/usr/bin/env python3
"""
Database Configuration Switcher for BroCode Challenge Platform
Easily switch between different database environments
"""

import os
import sys

def switch_to_sqlite():
    """Switch to SQLite configuration"""
    env_content = """# Database Configuration
# Currently using: SQLite (Development)
DATABASE_URL=sqlite:///./brocode.db

# Alternative configurations:
# Local PostgreSQL: postgresql://brocode_user:your_password@localhost:5432/brocode_db
# Remote Server: postgresql://brocode_user:competition_password@your-server.com:5432/brocode_competition

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Challenge Configuration
CHALLENGE_DURATION_MINUTES=180
MAX_QUESTIONS=30

# File Upload Configuration
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=.homie
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Switched to SQLite configuration")
    print("   DATABASE_URL=sqlite:///./brocode.db")
    return True

def switch_to_local_postgres(password="your_password"):
    """Switch to local PostgreSQL configuration"""
    env_content = f"""# Database Configuration
# Currently using: Local PostgreSQL
DATABASE_URL=postgresql://brocode_user:{password}@localhost:5432/brocode_db

# Alternative configurations:
# SQLite (Development): sqlite:///./brocode.db
# Remote Server: postgresql://brocode_user:competition_password@your-server.com:5432/brocode_competition

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Challenge Configuration
CHALLENGE_DURATION_MINUTES=180
MAX_QUESTIONS=30

# File Upload Configuration
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=.homie
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Switched to Local PostgreSQL configuration")
    print(f"   DATABASE_URL=postgresql://brocode_user:{password}@localhost:5432/brocode_db")
    print("   Make sure PostgreSQL is running and the database/user exists!")
    return True

def switch_to_remote_postgres(host="your-server.com", password="competition_password"):
    """Switch to remote PostgreSQL configuration"""
    env_content = f"""# Database Configuration
# Currently using: Remote PostgreSQL (Competition)
DATABASE_URL=postgresql://brocode_user:{password}@{host}:5432/brocode_competition

# Alternative configurations:
# SQLite (Development): sqlite:///./brocode.db
# Local PostgreSQL: postgresql://brocode_user:your_password@localhost:5432/brocode_db

# JWT Configuration
SECRET_KEY=your-production-secret-key-change-this-for-competition
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=False
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://your-competition-domain.com

# Challenge Configuration
CHALLENGE_DURATION_MINUTES=180
MAX_QUESTIONS=30

# File Upload Configuration
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=.homie
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Switched to Remote PostgreSQL configuration")
    print(f"   DATABASE_URL=postgresql://brocode_user:{password}@{host}:5432/brocode_competition")
    print("   ⚠️  Make sure the remote server is accessible and SSL is enabled!")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python switch_database.py <option>")
        print("\nOptions:")
        print("  sqlite              - Switch to SQLite (development)")
        print("  local [password]    - Switch to local PostgreSQL")
        print("  remote [host] [pwd] - Switch to remote PostgreSQL")
        print("\nExamples:")
        print("  python switch_database.py sqlite")
        print("  python switch_database.py local mypassword")
        print("  python switch_database.py remote myserver.com comp_pass")
        return
    
    option = sys.argv[1].lower()
    
    if option == "sqlite":
        success = switch_to_sqlite()
    elif option == "local":
        password = sys.argv[2] if len(sys.argv) > 2 else "your_password"
        success = switch_to_local_postgres(password)
    elif option == "remote":
        host = sys.argv[2] if len(sys.argv) > 2 else "your-server.com"
        password = sys.argv[3] if len(sys.argv) > 3 else "competition_password"
        success = switch_to_remote_postgres(host, password)
    else:
        print(f"❌ Unknown option: {option}")
        return
    
    if success:
        print("\n💡 Next steps:")
        print("   1. If switching to PostgreSQL, run: pip install psycopg2-binary")
        print("   2. Run: python setup_database.py")
        print("   3. Start server: python server.py")

if __name__ == "__main__":
    main()
