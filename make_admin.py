#!/usr/bin/env python3
"""
Quick script to make a user admin for testing purposes
"""
import sys
import os
sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.user.model import User

# Create database session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def make_user_admin(username: str):
    """Make a user admin"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            user.role = "admin"
            db.commit()
            print(f"User '{username}' is now an admin!")
        else:
            print(f"User '{username}' not found")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    make_user_admin(username)
