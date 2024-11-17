# backend/seeder.py
from database import SessionLocal, engine
import models
from utils.hasher import CustomHasher
import random
from datetime import datetime, timedelta

def seed_users():
    db = SessionLocal()
    hasher = CustomHasher()
    
    # Sample user data
    users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "is_admin": True
        },
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "john123",
            "is_admin": False
        },
        {
            "username": "jane_doe",
            "email": "jane@example.com",
            "password": "jane123",
            "is_admin": False
        },
        {
            "username": "test_user",
            "email": "test@example.com",
            "password": "test123",
            "is_admin": False
        }
    ]
    
    print("Starting user seeding...")
    
    try:
        for user_data in users:
            # Check if user already exists
            existing_user = db.query(models.User).filter(
                models.User.username == user_data["username"]
            ).first()
            
            if existing_user:
                print(f"User {user_data['username']} already exists, skipping...")
                continue
            
            # Try truncating hash first
            password_hash = hasher.truncate_hash(user_data["password"])
            hash_method = "truncate"
            
            # Check for collision
            if db.query(models.User).filter(models.User.password_hash == password_hash).first():
                # Try folding hash
                password_hash = hasher.folding_hash(user_data["password"])
                hash_method = "folding"
                
                # If still collision, use open hashing
                attempt = 0
                while db.query(models.User).filter(models.User.password_hash == password_hash).first():
                    password_hash = hasher.open_hash(user_data["password"], attempt)
                    hash_method = f"open_{attempt}"
                    attempt += 1
            
            # Create new user
            new_user = models.User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=password_hash,
                hash_method=hash_method
            )
            
            db.add(new_user)
            print(f"Added user: {user_data['username']}")
            
        db.commit()
        print("User seeding completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        db.rollback()
    finally:
        db.close()

def clear_database():
    db = SessionLocal()
    try:
        print("Clearing existing data...")
        db.query(models.User).delete()
        db.commit()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"Error clearing database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeder...")
    
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Ask user if they want to clear existing data
    clear = input("Do you want to clear existing data? (y/n): ").lower()
    if clear == 'y':
        clear_database()
    
    # Run seeders
    seed_users()
    
    print("Seeding completed!")