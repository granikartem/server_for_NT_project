from typing import List, Union

from pydantic import BaseModel


class VideoBase(BaseModel):
    url: str
    assigned_class: str


class VideoCreate(VideoBase):
    anger_percentage: float
    disgust_percentage: float
    fear_percentage: float
    joy_percentage: float
    neutral_percentage: float
    sadness_percentage: float
    surprise_percentage: float


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True
