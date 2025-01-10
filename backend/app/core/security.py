from datetime import datetime, timedelta
from typing import Optional, Union, Dict, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, validator
import logging
from .config import settings

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Security contexts
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: bool = False
    scopes: List[str] = []

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class User(UserBase):
    id: str

class UserInDB(User):
    hashed_password: str

# Security Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None,
    additional_claims: Dict = None
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    if additional_claims:
        to_encode.update(additional_claims)
        
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        logger.debug(f"Created access token for user: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise

# Authentication Functions
async def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with username and password"""
    try:
        # In practice, fetch user from database
        user = {
            "id": "1",
            "username": username,
            "email": f"{username}@example.com",
            "full_name": "Test User",
            "disabled": False,
            "hashed_password": get_password_hash(password),
            "scopes": ["user"]
        }
        
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
            
        return UserInDB(**user)
    except Exception as e:
        logger.error(f"Error authenticating user: {str(e)}")
        return None

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme)
) -> UserInDB:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate JWT token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
        
        # In practice, fetch user from database
        user = {
            "id": "1",
            "username": token_data.username,
            "email": f"{token_data.username}@example.com",
            "full_name": "Test User",
            "disabled": False,
            "hashed_password": "mock_hashed_password",
            "scopes": token_data.scopes
        }
        
        if user is None:
            raise credentials_exception
            
        # Log access attempt
        logger.info(f"User {username} accessed {request.url.path}")
        return UserInDB(**user)
        
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise credentials_exception

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Check if current user is active"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def check_permissions(required_scopes: List[str]):
    """Decorator to check user permissions"""
    async def permission_dependency(user: User = Depends(get_current_active_user)):
        for scope in required_scopes:
            if scope not in user.scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required scope: {scope}"
                )
        return user
    return permission_dependency

# Rate Limiting
class RateLimiter:
    def __init__(self):
        self.requests = {}
        
    async def check_rate_limit(self, user_id: str):
        """Check if user has exceeded rate limit"""
        now = datetime.utcnow()
        user_requests = self.requests.get(user_id, [])
        
        # Remove old requests
        user_requests = [
            req_time for req_time in user_requests 
            if now - req_time < timedelta(minutes=1)
        ]
        
        if len(user_requests) >= settings.RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
            
        user_requests.append(now)
        self.requests[user_id] = user_requests

rate_limiter = RateLimiter()