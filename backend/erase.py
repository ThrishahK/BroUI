#!/usr/bin/env python3
"""
Data Cleanup Script for BroCode
Erases all submissions and sessions, and resets team scores.
Preserves Teams and Questions.
"""

import os
import sys
from sqlalchemy import text

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Submission, ChallengeSession, Team

def erase_data():
    print("🧹 Starting Data Cleanup...")
    db = SessionLocal()
    
    try:
        # 1. Delete Submissions
        print("   Removing all submissions...")
        num_submissions = db.query(Submission).delete()
        print(f"   ✅ Deleted {num_submissions} submissions")

        # 2. Delete Sessions
        print("   Removing all challenge sessions...")
        num_sessions = db.query(ChallengeSession).delete()
        print(f"   ✅ Deleted {num_sessions} sessions")

        # 3. Reset Team Scores
        print("   Resetting team scores to 0...")
        # Update all teams to score 0
        teams = db.query(Team).all()
        for team in teams:
            team.score = 0
        
        print(f"   ✅ Reset scores for {len(teams)} teams")

        db.commit()
        print("\n✨ Wipe Complete! All test data has been erased.")
        print("   You can now start fresh.")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Cleanup failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    confirm = input("⚠️  Are you sure you want to ERASE all progress? (y/n): ")
    if confirm.lower() == 'y':
        erase_data()
    else:
        print("Cancelled.")
