from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas


def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_videos(db: Session):
    return db.query(models.Video).all()

def get_videos_by_class(db: Session, assigned_class: str):
    return db.query(models.Video).filter(models.Video.assigned_class == assigned_class).all()


def create_video(db: Session, video: schemas.Video):
    db_video = models.Video(url = video.url,
                            assigned_class = video.assigned_class,
                            anger_percentage = video.anger_percentage,
                            disgust_percentage = video.disgust_percentage,
                            fear_percentage = video.fear_percentage,
                            joy_percentage = video.joy_percentage,
                            neutral_percentage = video.neutral_percentage,
                            sadness_percentage = video.sadness_percentage,
                            surprise_percentage = video.surprise_percentage,
                            time_added = datetime.now())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def delete_old_videos(db: Session):
    week_ago = datetime.now() - timedelta(days = 7)
    db.query(models.Video).filter(models.Video.time_added < week_ago).delete()
    db.commit()