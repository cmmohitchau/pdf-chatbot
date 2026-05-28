from fastapi import APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests

from db.model import User
from db.crud import get_user_by_email
from db.engine import SessionDep
from core.security import create_access_token
from datetime import timedelta
from config.config import GOOGLE_CLIENT_ID

from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    id_token: str

router = APIRouter()


@router.post("/auth/google")
async def google_auth(
    data: GoogleAuthRequest,
    session: SessionDep
):
    try:
        # Verify token with Google
        google_user = id_token.verify_oauth2_token(
            data.id_token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        print(f"Google token verified. User info: {google_user}")

        if not google_user["email_verified"]:
            raise HTTPException(
                status_code=401,
                detail="Email not verified"
            )

        email = google_user["email"]
        name = google_user.get("name")

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google token"
        )

    # Find existing user
    user = get_user_by_email(
        session=session,
        email=email
    )
    print(f"Google auth - email: {email}, name: {name}, existing user: {user}")

    # Create new user if not exists
    if not user:
        user = User(
            email=email,
            name=name
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    # Create YOUR app JWT
    access_token = create_access_token(
        user.id,
        timedelta(weeks=2)
    )

    print(f"User {email} authenticated via Google. User ID: {user.id}")
    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }
