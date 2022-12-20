from sqlalchemy import Column, Integer, String
from database import Base


# create a user class in orm language
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    exp_group = Column(Integer, nullable=False)
    os = Column(String, nullable=False)
    source = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.id}"

