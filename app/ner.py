import spacy

model = spacy.load('ru_core_news_lg')

def ner(text):
    result = {'PER': [], 'ORG': [], 'LOC': []}

    for ent in model(text).ents:
        result[ent.label_] += [ent.text]
    
    return result