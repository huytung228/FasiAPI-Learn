from sqlalchemy import Column, Integer, String
import database


class Blogs(database.Base):
    __tablename__ = "Blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    
class User(database.Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)