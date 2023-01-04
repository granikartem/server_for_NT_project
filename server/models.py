from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from server.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    assigned_class = Column(String)
    anger_percentage = Column(Float)
    disgust_percentage = Column(Float)
    fear_percentage = Column(Float)
    joy_percentage = Column(Float)
    neutral_percentage = Column(Float)
    sadness_percentage = Column(Float)
    surprise_percentage = Column(Float)
    time_added = Column(DateTime)