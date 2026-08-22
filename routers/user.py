from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
import db_model
from models import CreateUser, UserResponse
from database import SessionLocal
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
user_router = APIRouter()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "your-secret-key-here" 
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")



async def get_current_user(token:str=Depends(oauth2_scheme) ,db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY ,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Invalid Token")
        user = db.query(db_model.UserDB).filter(db_model.UserDB.username == username).first()
        if user is None :
            raise HTTPException(status_code=401,detail="User Not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
        
    



@user_router.post("/registerUser", response_model=UserResponse)
async def register(new_user:CreateUser,db:Session = Depends(get_db)):
    existing = db.query(db_model.UserDB).filter(db_model.UserDB.username == new_user.username).first()
    if (existing):
        raise HTTPException(status_code=400,detail="User already Registered")
    db_user = db_model.UserDB(username= new_user.username , hashed_password= pwd_context.hash(new_user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.post("/login")
async def login(from_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    existing = db.query(db_model.UserDB).filter(db_model.UserDB.username == from_data.username).first()
    if not existing:
        raise HTTPException(status_code=400 ,detail="User Does Not exist")
    if not pwd_context.verify(from_data.password,existing.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect password")
    token= jwt.encode({"sub":from_data.username},SECRET_KEY ,algorithm=ALGORITHM)
    return {"access_token":token ,"token_type":"bearer"}







