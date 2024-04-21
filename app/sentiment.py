from transformers import pipeline

model_sentiment = pipeline(model="MonoHime/rubert-base-cased-sentiment-new")

def sentiment(text):
    result = model_sentiment(text[:256])[0]['label']
    if result == 'NEUTRAL':
        return 'Нейтральная'
    if result == 'POSITIVE':
        return 'Позитивная'
    if result == 'NEGATIVE':
        return 'Негативная'
