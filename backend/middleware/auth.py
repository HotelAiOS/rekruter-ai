from fastapi import Depends, HTTPException, status
from services.auth import get_current_active_user
from models import User

async def require_auth(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user

async def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
