from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token


def register_user(db: Session, user: UserCreate):

    try:
        # Check if the username or email already exists
        db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if db_user:
            if db_user.username == user.username:
                raise ValueError("Username already exists")
            if db_user.email == user.email:
                raise ValueError("Email already exists")

        # Create a new user
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise ValueError("Registration failed due to a database error")
def authenticate_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return None
    return db_user