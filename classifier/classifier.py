import asyncio
from sqlalchemy.orm import Session
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, BertTokenizer, TrainingArguments
from server.database import SessionLocal
from server import crud, schemas
from scrapper import scrapper, comment_scrapper
import numpy as np
import torch



class BackgroundClassifier:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        self.tokenizer = tokenizer
        model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base").to(device)
        default_args = {
            "output_dir": "tmp",
        }
        training_args = TrainingArguments(per_device_eval_batch_size=64, **default_args)
        self.model = model
        self.trainer = Trainer(self.model, training_args)



    async def run_classifier_routine(self):
        while True:
            print('data update')
            db = SessionLocal()
            torch.cuda.empty_cache()
            self.classifier_routine(db)
            crud.delete_old_videos(db)
            db.close()
            print('data updated')
            await asyncio.sleep(3600)


    def classifier_routine(self, db: Session):
        videos = set(scrapper.get_videos())
        server_videos = crud.get_videos(db)
        for s_video in server_videos:
            if s_video.url in videos:
                videos.remove(s_video.url)
        for video in videos:
            self.classify_video(video, db)

    def classify_video(self, video, db: Session):
        comments = comment_scrapper.get_comments(video)
        if(len(comments) > 0):
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
