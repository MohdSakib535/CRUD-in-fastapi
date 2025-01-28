from fastapi import APIRouter,Depends,HTTPException,status
import schemas
from fastapi.security import OAuth2PasswordRequestForm
import database
from sqlalchemy.orm import Session
import models
from hashing import Hash
import jwt_token

router=APIRouter(
    tags=["authentication"],
)

@router.post("/login/")
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(database.get_db)):
    user_data=db.query(models.User).filter(models.User.email == request.username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    if not Hash.verify(user_data.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Password")
    
    #generate jwt token
    access_token = jwt_token.create_access_token(data={"sub":user_data.email})
    return {"access_token":access_token,"token_type":"bearer"}



