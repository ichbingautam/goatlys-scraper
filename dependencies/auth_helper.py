from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config.db_config import Config

security = HTTPBearer()

def get_current_user(security_token: str = Depends(security)):
    print(security_token.credentials)
    if security_token.credentials != Config.STATIC_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return security_token