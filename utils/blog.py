import models
from sqlalchemy.orm import Session
import schemas



def get_all_blogs(db: Session):
    return db.query(models.Blog).all()


def create_blog_data(request: schemas.Blog,db:Session):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog