
from fastapi import APIRouter,Depends,HTTPException,status,Response
import database
import schemas
import models
from sqlalchemy.orm import Session
from hashing import Hash
from typing import List

user_router = APIRouter(
    tags=["users"],
)



@user_router.post("/createUser/", status_code=status.HTTP_201_CREATED, response_model=schemas.User,)
def Create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()  # Attempt to commit the transaction
    db.refresh(new_user)  # Refresh the session to get the new user details
    return new_user
    


@user_router.get("/all_users",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def all_users(db:Session = Depends(database.get_db)):
    return db.query(models.User).all()

@user_router.get("/user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def show_user(id:int,db:Session = Depends(database.get_db)):
    user_data=db.query(models.User).filter(models.User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not available") 
    return user_data
