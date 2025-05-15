from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

TOKEN_SCHEME = HTTPBearer()

class Authorization(BaseModel):
    token:HTTPAuthorizationCredentials = Security(TOKEN_SCHEME)