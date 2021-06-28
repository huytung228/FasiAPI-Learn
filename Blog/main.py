from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.sql.expression import false
import schema
import uvicorn
import models
import database
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from .models import User

models.database.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def add_blog(blog: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blogs(title = blog.title, content = blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schema.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schema.ShowBlog)
def get_blog(id : int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with {id} not existed')
    return blog

@app.delete('/blog/{id}', response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).delete(synchronize_session=False)
    db.commit()
    return None

@app.put('/blog/{id}', response_class=Response, status_code=status.HTTP_202_ACCEPTED)
def update(id: int, blog: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Can find blog with id= {id}")
    
    blog.update(blog)
    db.commit()
    return 'Update success'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/User', response_model=schema.ShowUser)
def add_user(user: schema.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Show user
@app.get('/user/{id}', status_code=200, response_model=schema.ShowUser)
def get_user(id : int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'can not find user with id = {id}')
    return user

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
