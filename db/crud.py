from db.model import UserCreate
from core.security import get_hash_password , verify_password , create_access_token , verify_access_token
from db.model import User
from config.config import JWT_SECRET
from db.engine import SessionDep
from sqlmodel import select
from datetime import timedelta

def sign_user(*, session: SessionDep, user: UserCreate):
    db_user = get_user_by_email(session=session, email=user.email)

    if not db_user:
        return None
    
    verified, updated_password_hash = verify_password(user.password, db_user.hashed_password)
    
    if not verified:
        return None

    jwt_token = create_access_token(db_user.email,timedelta(weeks=2))

    return jwt_token

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
    return db_obj

def get_user_by_email(*, session: SessionDep, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def jwt_authenticate(jwt_token : str):
    return verify_access_token(jwt_token)
