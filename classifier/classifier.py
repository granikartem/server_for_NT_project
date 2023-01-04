import asyncio
from sqlalchemy.orm import Session
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
from server.database import SessionLocal
from server import crud, schemas
import numpy as np
from pydantic import BaseModel

class BackgroundClassifier:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        self.trainer = Trainer(self.model)

    async def run_classifier_routine(self):
        while True:
            print('data update')
            db = SessionLocal()
            ##self.classifier_routine(db)
            crud.delete_old_videos(db)
            db.close()
            await asyncio.sleep(3600)

    def classifier_routine(self, db: Session):
        ##videos = get_videos()
        videos = ['ama,a,msammsan']
        for video in videos:
            self.classify_video(video, db)

    def classify_video(self, video, db: Session):
        ##comments = video.get_comments()
        comments = ['I like that', 'That is annoying', 'This is great!', 'Wouldn´t recommend it.']
        tokenized_comments = self.tokenizer(comments, truncation = True, padding = True)
        comments_dataset = SimpleDataset(tokenized_comments)
        classified_comments = self.trainer.predict(comments_dataset)
        scores = (np.exp(classified_comments[0]) / np.exp(classified_comments[0]).sum(-1, keepdims=True)).transpose()
        emotion_scores = []
        emotion_scores.append(scores[0].mean())
        emotion_scores.append(scores[1].mean())
        emotion_scores.append(scores[2].mean())
        emotion_scores.append(scores[3].mean())
        emotion_scores.append(scores[4].mean())
        emotion_scores.append(scores[5].mean())
        emotion_scores.append(scores[6].mean())
        assigned_class = self.model.config.id2label[emotion_scores.index(max(emotion_scores))]
        db_video = schemas.Video(url = video,
                                 assigned_class=assigned_class,
                                 anger_percentage = emotion_scores[0],
                                 disgust_percentage = emotion_scores[1],
                                 fear_percentage = emotion_scores[2],
                                 joy_percentage = emotion_scores[3],
                                 neutral_percentage = emotion_scores[4],
                                 sadness_percentage = emotion_scores[5],
                                 surprise_percentage = emotion_scores[6]
                                 )
        crud.create_video(db, db_video)

class SimpleDataset:
    def __init__(self, tokenized_texts):
        self.tokenized_texts = tokenized_texts

    def __len__(self):
        return len(self.tokenized_texts["input_ids"])

    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.tokenized_texts.items()}
