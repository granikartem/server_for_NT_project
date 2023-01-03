import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification


tokenizer = AutoTokenizer.from_pretrained("Jorgeutd/sagemaker-roberta-base-emotion")

model = AutoModelForSequenceClassification.from_pretrained("Jorgeutd/sagemaker-roberta-base-emotion")

data = pd.read_csv('small.csv', error_bad_lines=False )
comments = data['comment_text']
for comment in comments:
    if len(comment) < 512:
        print(comment)
        inputs = tokenizer(comment, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_class_id = logits.argmax().item()
        print(model.config.id2label[predicted_class_id])
        print(model.config.id2label)
        print(logits.softmax(dim=-1).tolist())


import asyncio
import uvicorn

async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })

async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())


