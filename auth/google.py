
from db.model import UserBase
from db.crud import get_user_by_email
from db.engine import SessionDep
from db.model import User
from core.security import create_access_token
from fastapi import APIRouter
from datetime import timedelta

router = APIRouter()

@router.post("/auth/google")
async def google_auth(data: UserBase, session : SessionDep):
    print("data in backend : " , data)
    user = get_user_by_email(session=session , email=data.email)

    if not user:
        user = User(
            email=data.email,
            name=data.name
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    
    access_token = create_access_token(
        user.id,
        timedelta(weeks=2)
    )

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }