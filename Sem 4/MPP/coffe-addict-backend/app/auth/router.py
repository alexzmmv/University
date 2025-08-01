from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.schemas import (
    UserCreate, UserResponse, Token, RefreshTokenRequest, 
    TwoFactorVerificationRequest, LoginResponse, LoginRequest
)
from app.auth.service import (
    create_user, login_user, get_user_response, refresh_access_token,
    complete_2fa_login
)
from app.auth.jwt import get_current_active_user
from app.database.models.models import User

router = APIRouter(tags=["authentication"], prefix="/auth")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    db_user = create_user(db, user)
    return get_user_response(db_user)

@router.post("/token", response_model=LoginResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Get access token for login (with 2FA support)
    """
    return login_user(db, form_data.username, form_data.password)

@router.post("/login", response_model=LoginResponse)
def login_endpoint(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint that supports 2FA
    """
    return login_user(db, login_data.username, login_data.password)

@router.post("/verify-2fa", response_model=LoginResponse)
def verify_2fa(verification_data: TwoFactorVerificationRequest, db: Session = Depends(get_db)):
    """
    Verify 2FA code and complete login
    """
    # For now, we'll use the verify_2fa_and_login function since we don't store username with job_id
    # In a production system, you might want to store user info with the verification code
    from app.auth.service import verify_2fa_and_login
    return verify_2fa_and_login(db, verification_data.job_id, verification_data.code)

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Use a refresh token to get a new access token
    """
    tokens = refresh_access_token(db, refresh_request.refresh_token)
    # Keep the original refresh token
    return {
        "access_token": tokens["access_token"],
        "refresh_token": refresh_request.refresh_token,
        "token_type": tokens["token_type"]
    }

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information
    """
    return get_user_response(current_user)
