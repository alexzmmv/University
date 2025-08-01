from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status
from datetime import timedelta
from jose import JWTError, jwt

from app.database.models.models import User
from app.auth.password import verify_password, get_password_hash
from app.auth.schemas import UserCreate, UserResponse, TokenData, TwoFactorResponse, LoginResponse
from app.auth.jwt import create_access_token, create_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.auth.sms_service import sms_service

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get a user by username
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user
    """
    # Check if username already exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Check if email already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        phone_number=user.phone_number,
        enable_2fa=user.enable_2fa,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

def login_user(db: Session, username: str, password: str) -> LoginResponse:
    """
    Login a user and return access token or 2FA challenge
    """
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user has 2FA enabled
    if user.enable_2fa:
        # Send 2FA code
        try:
            job_id = sms_service.send_verification_code(user.phone_number, user.username)
            # Hide most of the phone number for security
            phone_hint = f"***-***-{user.phone_number[-4:]}" if len(user.phone_number) >= 4 else "***"
            
            return LoginResponse(
                requires_2fa=True,
                job_id=job_id,
                message="A verification code has been sent to your phone",
                phone_number_hint=phone_hint
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send verification code: {str(e)}"
            )
    else:
        # Regular login without 2FA
        return _create_login_tokens(user)

def verify_2fa_and_login(db: Session, job_id: str, code: str) -> LoginResponse:
    """
    Verify 2FA code and complete login
    """
    # Get username from job_id
    username = sms_service.get_username_from_job(job_id)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification session"
        )
    
    # Verify the code
    is_valid = sms_service.verify_code(job_id, code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification code"
        )
    
    # Get user and create tokens
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return _create_login_tokens(user)

def complete_2fa_login(db: Session, username: str, job_id: str, code: str) -> LoginResponse:
    """
    Complete 2FA login process - verify code and create tokens
    """
    # First verify the 2FA code
    is_valid = sms_service.verify_code(job_id, code)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification code"
        )
    
    # Get user and create tokens
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return _create_login_tokens(user)

def _create_login_tokens(user: User) -> LoginResponse:
    """
    Helper function to create login tokens
    """
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.public_id},
        expires_delta=access_token_expires,
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(data={"sub": user.public_id})
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        requires_2fa=False
    )

def refresh_access_token(db: Session, refresh_token: str):
    """
    Use a refresh token to generate a new access token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        # Verify it's a refresh token
        if user_id is None or token_type != "refresh":
            raise credentials_exception
        
        # Check if user exists
        user = db.query(User).filter(User.public_id == user_id).first()
        if user is None:
            raise credentials_exception
        
        # Create new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires,
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        raise credentials_exception

def get_user_response(user: User) -> UserResponse:
    """
    Convert User model to UserResponse schema
    """
    return UserResponse(
        public_id=user.public_id,
        email=user.email,
        username=user.username,
        phone_number=user.phone_number,
        enable_2fa=user.enable_2fa,
        is_active=user.is_active,
        created_at=user.created_at,
    )
