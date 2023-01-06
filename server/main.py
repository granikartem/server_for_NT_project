from typing import List
import asyncio
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from classifier import classifier
from server import models, schemas,util
from server import crud
from server.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

background_classifier = classifier.BackgroundClassifier()

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(background_classifier.run_classifier_routine())

@app.get("/video")
def start_page(assigned_class: str,
               anger: float,
               disgust: float,
               fear: float,
               joy: float,
               neutral: float,
               sad: float,
               surprise: float,
               db: Session = Depends(get_db)):
    videos = crud.get_videos(db)
    return util.find_best_video(videos, anger, disgust, fear, joy, neutral, sad, surprise)
