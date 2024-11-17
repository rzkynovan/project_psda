from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from schemas import UserCreate, UserLogin
from utils.hasher import CustomHasher

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registration endpoint
@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Try truncating hash first
    hasher = CustomHasher()
    password_hash = hasher.truncate_hash(user.password)
    hash_method = "truncate"
    
    # Check for collision
    if db.query(models.User).filter(models.User.password_hash == password_hash).first():
        # Try folding hash
        password_hash = hasher.folding_hash(user.password)
        hash_method = "folding"
        
        # If still collision, use open hashing
        attempt = 0
        while db.query(models.User).filter(models.User.password_hash == password_hash).first():
            password_hash = hasher.open_hash(user.password, attempt)
            hash_method = f"open_{attempt}"
            attempt += 1
    
    # Create new user
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        hash_method=hash_method
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User registered successfully"}

# Login endpoint
@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Get hash method used for this user
    hash_method = db_user.hash_method
    hasher = CustomHasher()
    
    # Generate hash based on stored method
    if hash_method == "truncate":
        password_hash = hasher.truncate_hash(user.password)
    elif hash_method == "folding":
        password_hash = hasher.folding_hash(user.password)
    elif hash_method.startswith("open_"):
        attempt = int(hash_method.split("_")[1])
        password_hash = hasher.open_hash(user.password, attempt)
    
    if password_hash != db_user.password_hash:
        raise HTTPException(status_code=400, detail="Invalid password")
    
    return {"message": "Login successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)