from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    content: str

class ShowBlog(BaseModel):
    title: str
    class Config():
        orm_mode =True
    
class User(BaseModel):
    username: str
    email: str
    password: str

class ShowUser(BaseModel):
    username: str
    email: str
    class Config():
        orm_mode =True