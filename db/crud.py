from db.model import UserCreate
from core.security import get_hash_password , verify_password , create_access_token , verify_access_token
from db.model import User
from config.config import JWT_SECRET
from db.engine import SessionDep
from datetime import timedelta
from sqlmodel import select

def sign_user(*, session: SessionDep, user: UserCreate):
    db_user = get_user_by_email(session=session, email=user.email)

    if not db_user:
        return None
    
    verified, updated_password_hash = verify_password(user.password, db_user.hashed_password)
    
    if not verified:
        return None

    access_token = create_access_token(db_user.id,timedelta(weeks=2))


    return {
        "access_token": access_token,
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name
        }
    }

def create_user(*, session: SessionDep, user : UserCreate):
    db_user = get_user_by_email(session=session ,email=user.email)

    if db_user:
        return None
    
    db_obj = User.model_validate(
        user, update={"hashed_password" : get_hash_password(password=user.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return {
        "message" : "signup successfully"
    }

def get_user_by_email(*, session: SessionDep, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def jwt_authenticate(jwt_token : str):
    return verify_access_token(jwt_token)
