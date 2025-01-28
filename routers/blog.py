from fastapi import APIRouter,status,Depends,HTTPException,Response
import database
import models
from typing import List
import schemas
from sqlalchemy.orm import Session
from utils.blog import get_all_blogs ,create_blog_data
import oauth2
blog_router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)



"""
response_model: This parameter is used to define the Pydantic model that will be used to format the output data. This will ensure that the output data is formatted according to the schema defined in the Pydantic model.
"""

@blog_router.post("/createBlog/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def create_blog(request: schemas.Blog,db:Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return create_blog_data(request,db)



@blog_router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return get_all_blogs(db)



@blog_router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def show_blog(id:int,response:Response,db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog_data=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_data:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with id {id} is not available"}
        # or
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    return blog_data


@blog_router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request:schemas.Blog,db:Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog_data=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    # blog_data.update({"title":request.title,"body":request.body})
    # or   
    blog_data.update(request.dict(exclude_unset=True))  
    """
    request.dict(exclude_unset=True): This method is now the correct way to convert the Pydantic model to a dictionary, and exclude_unset=True ensures that only the provided fields are used for updating the model.
    """ 
    db.commit()
    return {"message":f"Blog  with id {id} updated successfully"}


@blog_router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog_data=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    db.delete(blog_data)
    db.commit()
    return "Blog deleted successfully"




"""
synchronize_session parameter is relevant only for bulk deletion or bulk update operations, such as when using the query.delete() or query.update() methods.
"""

@blog_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def bulk_delete_blogs(ids: List[int], db: Session = Depends(database.get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    # Bulk delete query
    rows_deleted = db.query(models.Blog).filter(models.Blog.id.in_(ids)).delete(synchronize_session=False)
    db.commit()

    # Check if any rows were deleted
    if rows_deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No blogs found for the given IDs"
        )

    return {"message": f"{rows_deleted} blog(s) deleted successfully"}