from fastapi import Depends, FastAPI, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import crud
import models
import schemas
from dependencies import get_db
from security import create_access_token, verify_password

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.post("/api/register", response_model=schemas.Token)
@limiter.limit("5/minute")
def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    crud.create_user(db=db, user=user)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/login", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(request: Request, user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/vk")
async def auth_vk():
    # Redirect user to VK for authentication
    return {"message": "Redirect to VK"}


@app.get("/api/auth/vk/callback")
async def auth_vk_callback():
    # Handle callback from VK
    return {"message": "VK callback"}


@app.get("/api/auth/sferum")
async def auth_sferum():
    # Redirect user to Sferum for authentication
    return {"message": "Redirect to Sferum"}


@app.get("/api/auth/sferum/callback")
async def auth_sferum_callback():
    # Handle callback from Sferum
    return {"message": "Sferum callback"}
