from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, utils, schemas
from ..outh2 import create_access_token

router = APIRouter(
    tags=["Auth"]
)


@router.post("/login", response_model=schemas.Token)
# def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(
        models.Users.email == payload.username).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify_password(payload.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": existing_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
