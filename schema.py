from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
Base = declarative_base()

class Listings(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    location = Column(String)
    size = Column(Float)
    rooms = Column(Integer)
    yard = Column(Float)
    url = Column(String)

    def __init__(self, title, price, location, size, rooms, yard, url):
        self.title = title
        self.price = price
        self.location = location
        self.size = size
        self.rooms = rooms
        self.yard = yard
        self.url = url

class UpdateLog(Base):
    __tablename__ = 'update_log'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    execute_time = Column(Float)
