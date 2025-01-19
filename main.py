from fastapi import FastAPI,Depends,status,Response,HTTPException
from pydantic import BaseModel
app = FastAPI()
import models
import schemas
import database
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=database.engine)



@app.post("/createBlog/",status_code=status.HTTP_201_CREATED)
def read_root(request: schemas.Blog,db:Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blogs/")
def all_blogs(db: Session = Depends(database.get_db)):
    return db.query(models.Blog).all()

@app.get("/blogs/{id}",status_code=status.HTTP_200_OK)
def show_blog(id:int,response:Response,db: Session = Depends(database.get_db)):
    blog_data=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_data:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with id {id} is not available"}
        # or
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    return blog_data


@app.put("/blogs/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request:schemas.Blog,db:Session = Depends(database.get_db)):
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


@app.delete("/blogs/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db: Session = Depends(database.get_db)):
    blog_data=db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} is not available")
    db.delete(blog_data)
    db.commit()
    return "Blog deleted successfully"



"""
synchronize_session parameter is relevant only for bulk deletion or bulk update operations, such as when using the query.delete() or query.update() methods.
"""

@app.delete("/blogs/", status_code=status.HTTP_204_NO_CONTENT)
def bulk_delete_blogs(ids: List[int], db: Session = Depends(database.get_db)):
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