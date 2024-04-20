from transformers import pipeline

model_sentiment = pipeline(model="MonoHime/rubert-base-cased-sentiment-new")

def sentiment(text):
    return model_sentiment(text)[0]['label']