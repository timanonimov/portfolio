from sqlalchemy import Column, Integer, String, Text
from database import Base


# create a post class in orm language
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    topic = Column(String, nullable=True)

    def __repr__(self):
        return f"{self.id} - {self.topic}"
