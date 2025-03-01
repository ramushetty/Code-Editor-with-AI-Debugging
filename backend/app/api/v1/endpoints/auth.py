from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token, get_current_user
from app.core.database import get_db

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):

    try:
        db_user = register_user(db, user)
    except ValueError as e:
        # Handle user-friendly errors (e.g., duplicate username or email)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail="Registration failed due to an unexpected error")

    # Generate a JWT token for the new user
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    print(db_user.id)
    access_token = create_access_token(data={"sub": str(db_user.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=False, secure=True, samesite="lax")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}

@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}