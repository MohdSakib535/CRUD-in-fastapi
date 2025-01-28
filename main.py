from fastapi import FastAPI,Depends,status,Response,HTTPException
from pydantic import BaseModel
import models
import schemas
import database
import uvicorn
from routers import blog,user,authentication
app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
# models.Base.metadata.drop_all(bind=database.engine)


app.include_router(blog.blog_router)
app.include_router(user.user_router)
app.include_router(authentication.router)




